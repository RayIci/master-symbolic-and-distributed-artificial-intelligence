#!/usr/bin/env python3
"""
Slides server with live ▶ execution
===================================
Serves the slides and lets the ▶ buttons really run the lab scripts, streaming their output.

    uv run slides/serve.py              # http://localhost:8080
    uv run slides/serve.py --port 9000 --no-browser

Only the lab scripts can be executed (steps/<step>/demo.py and steps/<step>/solution.py,
plus the Icaros demos demos/<demo>/<name>.mas2i), and the server only listens on 127.0.0.1.
The mock API (services/mock_api.py) is started automatically if it is not already running.

The Icaros demos run with the Icaros wheel bundled in demos/wheels/ (via uvx, Python 3.14
free-threaded; see demos/README.md), or with an Icaros checkout if ICAROS_HOME points to one
(default ../icaros-lang/icaros). Without uv the ▶ of those demos replays their recorded output instead.

Endpoints:
  /                      -> the slides (files of this folder)
  /api/health            -> {"status": "ok", "model": "..."}
  /api/run?script=...    -> runs the script, streams stdout+stderr as text
"""

import argparse
import functools
import json
import logging
import os
import re
import select
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

from lab.config import MOCK_API_URL, MODEL

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

SLIDES_DIR = Path(__file__).resolve().parent
REPO_ROOT = SLIDES_DIR.parent
RUNNABLE = re.compile(r"^(steps/[\w-]+/(demo|solution)\.py|demos/[\w-]+/[\w-]+\.mas2i)$")
ICAROS_HOME = Path(os.getenv("ICAROS_HOME", REPO_ROOT.parent / "icaros-lang" / "icaros")).expanduser()
ICAROS_WHEELS = sorted((REPO_ROOT / "demos" / "wheels").glob("icaros-*.whl"))


class Unavailable(Exception):
    """The script is allowed, but what it needs to run is not installed here."""


def resolve_script(script: str) -> Path | None:
    """Returns the path of an allowed script, or None."""
    if not RUNNABLE.match(script):
        return None
    path = (REPO_ROOT / script).resolve()
    if REPO_ROOT not in path.parents or not path.is_file():
        return None
    return path


def command_for(path: Path) -> tuple[list[str], dict]:
    """The command line (and environment) that runs an allowed script."""
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"}
    if path.suffix == ".py":
        return [sys.executable, "-u", str(path)], env
    # an Icaros multi-agent system: run it with Icaros' own environment (Python 3.14)
    if not shutil.which("uv"):
        raise Unavailable("uv not found: it is needed to run Icaros")
    env.pop("VIRTUAL_ENV", None)  # we run inside the lab's venv: do not hand it to Icaros
    if (ICAROS_HOME / "pyproject.toml").is_file():
        return ["uv", "run", "--quiet", "--project", str(ICAROS_HOME), "icaros", str(path), "--headless"], env
    if ICAROS_WHEELS:
        return ["uvx", "--quiet", "--python", "3.14t", "--from", f"{ICAROS_WHEELS[-1]}[ollama]",
                "icaros", str(path), "--headless"], env
    raise Unavailable(f"Icaros not found (no wheel in demos/wheels/, no checkout in {ICAROS_HOME})")


class SlidesHandler(SimpleHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, status):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self._send_json({"status": "ok", "model": MODEL})
        if parsed.path == "/api/run":
            script = parse_qs(parsed.query).get("script", [""])[0]
            return self._run(script)
        return super().do_GET()

    def _run(self, script: str):
        path = resolve_script(script)
        if path is None:
            return self._send_text(f"Not allowed: {script!r} (only steps/<step>/demo.py or solution.py, "
                                   "demos/<demo>/<name>.mas2i)\n", 400)
        try:
            cmd, env = command_for(path)
        except Unavailable as e:
            # the page falls back to the recorded output
            logging.info(f"▶ {script}: {e} -> replay")
            self.send_response(503)
            self.send_header("X-Fallback", "replay")
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"{e}\n".encode())
            return

        logging.info(f"▶ running {script}")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()  # HTTP/1.0 response: the body ends when we close the connection

        start = time.time()
        proc = subprocess.Popen(
            cmd,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,  # own process group: ■ Stop kills `uv run` AND what it started
        )
        # Pump the script output to the client in a thread, while this thread watches the socket:
        # when the client goes away (■ Stop, panel closed) the script is killed, even if it is
        # silently waiting for the LLM and has nothing to write.
        pump = threading.Thread(target=self._pump, args=(proc,), daemon=True)
        pump.start()
        try:
            while pump.is_alive():
                pump.join(0.3)
                if self._client_gone():
                    logging.info(f"■ {script} stopped by the client")
                    break
            else:
                code = proc.wait()
                if code != 0:
                    self.wfile.write(f"\n[exit code {code}]\n".encode())
                logging.info(f"■ {script} finished in {time.time() - start:.1f}s (exit code {code})")
        except (BrokenPipeError, ConnectionResetError):
            logging.info(f"■ {script} stopped by the client")
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()

    def _pump(self, proc):
        try:
            # read1 returns as soon as some output is available -> real-time streaming
            while chunk := proc.stdout.read1(4096):
                self.wfile.write(chunk)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ValueError):
            pass

    def _client_gone(self) -> bool:
        """True if the browser closed the connection (a closed socket is readable and returns b'')."""
        try:
            readable, _, _ = select.select([self.connection], [], [], 0)
            return bool(readable) and self.connection.recv(1, socket.MSG_PEEK) == b""
        except OSError:
            return True

    def log_message(self, fmt, *args):
        if not self.path.startswith("/api/"):
            return  # keep the console clean: log only the API calls
        logging.info("%s %s", self.command, self.path)


def ensure_mock_api() -> subprocess.Popen | None:
    """Starts services/mock_api.py if it is not already running (needed by steps 02 and 04)."""
    try:
        with urlopen(f"{MOCK_API_URL}/health", timeout=1) as r:
            if json.loads(r.read()).get("status") == "ok":
                logging.info(f"Mock API already running at {MOCK_API_URL}")
                return None
    except Exception:
        pass
    port = urlparse(MOCK_API_URL).port or 8765
    proc = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "services/mock_api.py"), "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    logging.info(f"Mock API started at {MOCK_API_URL} (pid {proc.pid})")
    return proc


def main():
    parser = argparse.ArgumentParser(description="Serve the lab slides with live ▶ execution")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the browser")
    args = parser.parse_args()

    # `kill` (SIGTERM) behaves like Ctrl+C, so the mock API we started is always stopped
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    mock = ensure_mock_api()
    handler = functools.partial(SlidesHandler, directory=str(SLIDES_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://localhost:{args.port}"
    logging.info(f"Slides: {url}   (model: {MODEL}, Ctrl+C to stop)")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down")
    finally:
        server.server_close()
        if mock:
            mock.terminate()


if __name__ == "__main__":
    main()
