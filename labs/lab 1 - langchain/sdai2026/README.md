# Agentic AI with local LLMs — SDAI 2026 lab

A hands-on, **incremental** lab (~2 hours) on **agentic AI**: starting from a single prompt and ending with
several LLMs that use tools inside a workflow, everything running **locally** with [Ollama](https://ollama.com),
[LangChain](https://python.langchain.com) and [LangGraph](https://langchain-ai.github.io/langgraph/).

| Time | Step | Folder | What you build |
|---|---|---|---|
| 10' | 00 · Setup | [`scripts/check_setup.py`](scripts/check_setup.py) | Ollama + model + Python environment |
| 20' | 01 · Chain | [`steps/01-chain`](steps/01-chain) | prompt → LLM → output parser, structured output |
| 30' | 02 · Tools | [`steps/02-tools`](steps/02-tools) | an agentic loop: the LLM calls Python functions and a REST API |
| 30' | 03 · Workflow | [`steps/03-workflow`](steps/03-workflow) | a LangGraph graph of collaborating LLMs, with a feedback loop |
| 25' | 04 · Agentic workflow | [`steps/04-agentic-workflow`](steps/04-agentic-workflow) | a workflow of agentic loops with specialised tools and a router |

The **slides** are in [`slides/`](slides/) — see [Slides](#slides) below.

## Setup (do it before the lab!)

All the commands below are typed in a terminal (macOS/Linux: *Terminal*; Windows: *PowerShell*).

1. **Install Ollama** from <https://ollama.com/download> and start it (open the Ollama app; on Linux it
   starts by itself). Ollama is the program that runs the LLMs on your computer. Check it with
   `ollama list`: it should print a (possibly empty) table, not an error.
2. **Download the model** (~2.5 GB, do it with a good connection):
   ```bash
   ollama pull qwen3:4b-instruct
   ```
3. **Install [uv](https://docs.astral.sh/uv/getting-started/installation/)**, the tool that installs Python
   and the lab's libraries for you:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh                                    # macOS / Linux
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
   ```
   Then close the terminal and open a new one, and check with `uv --version`.
4. **Unzip the lab and create the environment.** Download `sdai2026-lab.zip` from the course page, unzip it
   (double click, or `unzip sdai2026-lab.zip`): you get a folder `sdai2026` (Windows' *Extract All* may put
   it inside another folder, `sdai2026-lab\sdai2026`: use the inner one, the one with `README.md`). Then:
   ```bash
   cd sdai2026        # every command in this README is run from inside this folder
   uv sync            # downloads Python and the libraries into sdai2026/.venv (takes a minute)
   ```
   <details><summary>Without uv (if you really cannot install it)</summary>

   You need Python 3.11, 3.12 or 3.13:
   ```bash
   python3.12 -m venv .venv          # Windows: py -3.12 -m venv .venv
   source .venv/bin/activate         # Windows: .venv\Scripts\activate
   pip install -e .
   ```
   …and then use `python` wherever these instructions say `uv run`.
   </details>
5. **Check that everything works**:
   ```bash
   uv run scripts/check_setup.py
   ```
   Every line should say `[OK]`; if not, the script tells you what to fix.

### Using a different model
All scripts read the model from [`lab/config.py`](lab/config.py). To use another one, download it with
`ollama pull <model>` and set `LAB_MODEL`, without touching the code:
```bash
LAB_MODEL=llama3.2 uv run steps/02-tools/demo.py                     # macOS / Linux
$env:LAB_MODEL="llama3.2"; uv run steps/02-tools/demo.py             # Windows (PowerShell)
```
The model must support **tool calling**, i.e. it must be able to ask the program to run a function
(e.g. `qwen3`, `llama3.2`, `qwen2.5`, `mistral`). Prefer *instruct* models: *thinking* models (e.g. plain
`qwen3:4b`, `deepseek-r1`) reason for a long time before every tool call. Their reasoning is kept out of
the answers (see `LAB_REASONING` in `lab/config.py`).

## How each step works

Every folder in `steps/` contains:

- `README.md` — goal, concepts and the exercise text;
- `demo.py` — a complete, working example (run it first!);
- `exercise.py` — the starting point for the exercise, with `TODO` markers.

```bash
uv run steps/01-chain/demo.py
uv run steps/01-chain/exercise.py
```

Steps 02 and 04 also use a small fake REST API. Open a **second terminal**, go to the `sdai2026` folder
(`cd sdai2026`) and start it there; leave it running while you work (`Ctrl-C` stops it):
```bash
uv run services/mock_api.py
```

To run all the demos and save their outputs in `outputs/` (macOS/Linux only): `./scripts/run_all.sh`.

## Slides

```bash
uv run slides/serve.py        # http://localhost:8080 — the ▶ buttons really run the scripts
```
Every demo code block in the slides has a **▶** button: with `serve.py` it runs the corresponding
`steps/*/demo.py` on your machine and streams its output (the mock API is started automatically).
You can also just open `slides/index.html` in a browser (no build, no server): the ▶ buttons then
replay outputs recorded earlier, stored in `slides/recordings.js`. Optionally, to re-record them with your model:
```bash
uv run scripts/record_outputs.py
```

## Bonus: Icaros

The last slides show [Icaros](https://github.com/icaros-lang), a BDI multi-agent language whose agents can
hand a goal to an LLM. It is bundled in [`demos/`](demos/), with its own instructions: see
[`demos/README.md`](demos/README.md).

## Git: steps, your work, solutions

The folder you unzipped is a **git repository** (you need [git](https://git-scm.com/downloads) only for the
optional commands below):

- save your work as you go: `git add -A && git commit -m "exercise 02"`;
- each step is a **tag**: `git checkout step-02` shows you the repo as it was at the beginning of step 02,
  and `git checkout main` brings you back. Commit your work **before** switching, and only look around
  while you are on a tag: git warns you are in *detached HEAD*, and commits made there are easy to lose.

**Solutions.** After the lab you will receive `sdai2026-solutions.bundle` on the course page. Put it next to the
`sdai2026` folder and import it — your own commits are kept:
```bash
git add -A && git commit -m "my exercises"            # save your work first
git fetch ../sdai2026-solutions.bundle solutions:solutions
git checkout solutions                                 # steps/*/solution.py + solution slides
git diff main solutions -- steps/02-tools              # compare with your version
```
No git? The same solutions are also published as `sdai2026-solutions.zip`.

## Repository layout

```
├── lab/            # shared config (MODEL, URLs) and pretty-printing helpers
├── scripts/        # check_setup.py, run_all.sh, record_outputs.py, make_release.sh (teachers)
├── services/       # mock_api.py: a fake REST API used by the tools
├── steps/          # one folder per step
├── demos/          # Icaros demo shown at the end of the slides, with Icaros bundled (see demos/README.md)
└── slides/         # reveal.js slides (index.html) + serve.py for live ▶ execution
```
