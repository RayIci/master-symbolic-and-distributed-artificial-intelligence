#!/usr/bin/env python3
"""
Mock REST API for the lab
=========================
A tiny HTTP server with FAKE but deterministic data, so that our LLMs can use
"real" tools (HTTP calls) without API keys or internet access.

Usage (keep it running in a second terminal):
  uv run services/mock_api.py            # http://localhost:8765
  uv run services/mock_api.py --port 9000
  uv run services/mock_api.py --test     # quick self-test and exit

Endpoints:
  /                              -> HTML page listing the endpoints
  /health                        -> {"status": "ok"}
  /api/echo?msg=...              -> {"echo": "..."}
  /api/weather?city=Bologna      -> current (fake) weather for a city
  /api/search?q=AI medicine      -> (fake) web search results
  /api/stats?topic=ai adoption   -> (fake) statistical series about a topic
"""

import argparse
import hashlib
import json
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# ============================================
# FAKE DATA
# ============================================

WEATHER = {
    "bologna": {"temperature_c": 14, "condition": "fog", "humidity": 88, "wind_kmh": 5},
    "milan": {"temperature_c": 12, "condition": "cloudy", "humidity": 75, "wind_kmh": 8},
    "rome": {"temperature_c": 21, "condition": "sunny", "humidity": 55, "wind_kmh": 12},
    "naples": {"temperature_c": 22, "condition": "sunny", "humidity": 60, "wind_kmh": 15},
    "turin": {"temperature_c": 10, "condition": "rain", "humidity": 90, "wind_kmh": 6},
    "london": {"temperature_c": 9, "condition": "rain", "humidity": 85, "wind_kmh": 20},
    "paris": {"temperature_c": 13, "condition": "cloudy", "humidity": 70, "wind_kmh": 10},
    "new york": {"temperature_c": 16, "condition": "windy", "humidity": 50, "wind_kmh": 30},
}
CONDITIONS = ["sunny", "cloudy", "rain", "fog", "windy", "snow"]

DOCUMENTS = [
    {
        "title": "AI in diagnostic imaging",
        "keywords": ["ai", "medicine", "healthcare", "diagnosis", "imaging", "radiology"],
        "snippet": "Deep learning models reach 94% accuracy in detecting lung nodules on CT scans "
                   "and reduce the average reading time of radiologists by 30%.",
    },
    {
        "title": "FDA-cleared AI medical devices",
        "keywords": ["ai", "medicine", "healthcare", "fda", "devices", "regulation"],
        "snippet": "By 2024 the FDA had cleared more than 900 AI-enabled medical devices, "
                   "about 75% of them in radiology.",
    },
    {
        "title": "Machine learning for hospital readmissions",
        "keywords": ["machine learning", "healthcare", "hospital", "readmission", "prediction"],
        "snippet": "Predictive models flag high-risk patients at discharge and cut 30-day "
                   "readmissions by up to 25%.",
    },
    {
        "title": "AI-driven drug discovery",
        "keywords": ["ai", "drug", "discovery", "pharma", "medicine", "molecules"],
        "snippet": "Generative models shortened the pre-clinical phase of several drug candidates "
                   "from 4-5 years to about 18 months.",
    },
    {
        "title": "Risks of AI in healthcare",
        "keywords": ["ai", "healthcare", "risks", "bias", "privacy", "ethics"],
        "snippet": "Main concerns are dataset bias, patient privacy, lack of explainability "
                   "and unclear liability when a model is wrong.",
    },
    {
        "title": "Large language models in education",
        "keywords": ["llm", "ai", "education", "students", "teaching", "university"],
        "snippet": "In a 2025 survey 86% of university students reported using LLM assistants "
                   "for studying, mostly for explanations and summaries.",
    },
    {
        "title": "Energy consumption of AI",
        "keywords": ["ai", "energy", "climate", "data centers", "environment"],
        "snippet": "Data centers used about 1.5% of global electricity in 2024; AI workloads are "
                   "the fastest-growing share.",
    },
]

STATS = {
    "ai adoption": {
        "description": "Share of hospitals using at least one AI system (%)",
        "series": {"2020": 25, "2022": 45, "2024": 72},
    },
    "ai devices": {
        "description": "Cumulative number of FDA-cleared AI medical devices",
        "series": {"2018": 120, "2020": 340, "2022": 520, "2024": 950},
    },
    "ai market": {
        "description": "Global AI-in-healthcare market size (billion USD)",
        "series": {"2020": 6.7, "2022": 15.1, "2024": 26.6},
    },
    "llm usage students": {
        "description": "Share of university students using LLM assistants (%)",
        "series": {"2023": 43, "2024": 66, "2025": 86},
    },
}


def fake_weather(city: str) -> dict:
    """Known cities have fixed weather, unknown ones get a deterministic pseudo-random one."""
    key = city.strip().lower()
    if key in WEATHER:
        data = WEATHER[key]
    else:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        data = {
            "temperature_c": h % 35 - 5,
            "condition": CONDITIONS[h % len(CONDITIONS)],
            "humidity": 30 + h % 65,
            "wind_kmh": h % 40,
        }
    return {"city": city.strip().title(), **data}


STOPWORDS = {"a", "an", "and", "are", "for", "how", "in", "is", "of", "on", "or", "the", "to", "what", "with"}
SYNONYMS = {"artificial": "ai", "intelligence": "ai", "medical": "medicine", "hospitals": "hospital"}


def fake_search(query: str, limit: int = 3) -> dict:
    """Ranks the documents by number of query words matching their keywords/title."""
    words = {SYNONYMS.get(w, w) for w in query.lower().replace(",", " ").split()} - STOPWORDS
    scored = []
    for doc in DOCUMENTS:
        haystack = set(" ".join(doc["keywords"] + [doc["title"].lower()]).split())
        score = len(words & haystack)
        if score:
            scored.append((score, doc))
    scored.sort(key=lambda x: -x[0])
    results = [{"title": d["title"], "snippet": d["snippet"]} for _, d in scored[:limit]]
    return {"query": query, "results": results}


def fake_stats(topic: str) -> dict:
    key = topic.strip().lower()
    for name, data in STATS.items():
        if name in key or key in name:
            return {"topic": name, **data}
    return {"topic": topic, "error": "no statistics found", "available_topics": list(STATS)}


# ============================================
# HTTP SERVER
# ============================================

class MockHandler(BaseHTTPRequestHandler):
    def _send_json(self, obj, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        q = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            links = ["/health", "/api/echo?msg=hello", "/api/weather?city=Bologna",
                     "/api/search?q=AI medicine", "/api/stats?topic=ai adoption"]
            items = "".join(f"<li><a href='{l}'>{l}</a></li>" for l in links)
            self.wfile.write(f"<html><body><h1>Lab mock API</h1><ul>{items}</ul></body></html>".encode())
        elif path == "/health":
            self._send_json({"status": "ok"})
        elif path == "/api/echo":
            self._send_json({"echo": q.get("msg", "")})
        elif path == "/api/weather":
            if "city" not in q:
                return self._send_json({"error": "missing 'city' parameter"}, 400)
            self._send_json(fake_weather(q["city"]))
        elif path == "/api/search":
            if "q" not in q:
                return self._send_json({"error": "missing 'q' parameter"}, 400)
            self._send_json(fake_search(q["q"], int(q.get("limit", 3))))
        elif path == "/api/stats":
            if "topic" not in q:
                return self._send_json({"error": "missing 'topic' parameter"}, 400)
            self._send_json(fake_stats(q["topic"]))
        else:
            self._send_json({"error": "not found"}, 404)

    def log_message(self, fmt, *args):
        logging.info("%s %s", self.command, self.path)


def run_server(port: int):
    server = ThreadingHTTPServer(("", port), MockHandler)
    logging.info(f"Mock API listening on http://localhost:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server")
        server.shutdown()


def do_self_test(port: int, timeout: float = 5.0) -> bool:
    base = f"http://127.0.0.1:{port}"

    def fetch(path: str) -> dict:
        with urlopen(base + path.replace(" ", "%20"), timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    threading.Thread(target=run_server, args=(port,), daemon=True).start()
    time.sleep(0.3)

    try:
        assert fetch("/health") == {"status": "ok"}
        assert fetch("/api/echo?msg=test123")["echo"] == "test123"
        assert fetch("/api/weather?city=bologna")["condition"] == "fog"
        assert fetch("/api/weather?city=Atlantis") == fetch("/api/weather?city=Atlantis")
        assert fetch("/api/search?q=AI medicine")["results"]
        assert fetch("/api/stats?topic=AI adoption")["series"]["2024"] == 72
        return True
    except Exception as e:
        logging.error(f"Self-test failed: {e!r}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Mock REST API for the Agentic AI lab")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--test", action="store_true", help="Run self-test and exit")
    args = parser.parse_args()

    if args.test:
        ok = do_self_test(args.port)
        logging.info("Self-test passed" if ok else "Self-test failed")
        raise SystemExit(0 if ok else 1)

    run_server(args.port)


if __name__ == "__main__":
    main()
