# Bonus: Icaros

The last slides show **Icaros**, a language for **multi-agent systems** based on the **BDI** model
(*Belief–Desire–Intention*): each agent has *beliefs* (what it knows), *goals* (what it wants) and *plans*
(recipes that say how to reach a goal). The plans are written in **AgentSpeak**, and an Icaros agent can ask an
LLM for help when it has no plan for a goal.

This folder contains Icaros itself and one example agent, so you can run the demo of the slides on your own
computer. It is **optional**: you don't need it for the lab exercises.

```
demos/
├── wheels/icaros-0.1.0-py3-none-any.whl   # Icaros, as a Python package (do not unzip it)
└── icaros-barista/                        # the example: a barista agent
    ├── barista.mas2i                      #   the system: one agent, and which LLM it uses
    └── barista.asl                        #   the agent's plans, in AgentSpeak (read the comments!)
```

**The example.** The barista knows how to do the four steps of making a coffee (fetch the beans, grind them,
boil the water, brew), but it has **no plan for "make a coffee"**. So it hands the goal to the LLM, which decides
which step to ask for next, one at a time. Then the agent asks the LLM to explain what it did.

## What you need

You already have everything if you did the lab setup ([main README](../README.md#setup-do-it-before-the-lab)):

- **Ollama**, running, with the lab's model `qwen3:4b-instruct`;
- **uv**.

Icaros needs a newer Python than the lab: **Python 3.14 free-threaded** (written `3.14t`). **You don't have to
install it.** The first time you run the command below, uv downloads it on its own and installs Icaros in a
separate environment. Nothing changes in the lab's environment.

## Run it

Open a terminal **in the `sdai2026` folder** (the one you unzipped, which contains `README.md`) and run this
(it is one single command):

```bash
uvx --python 3.14t --from "demos/wheels/icaros-0.1.0-py3-none-any.whl[ollama]" icaros demos/icaros-barista/barista.mas2i --headless
```

What the parts mean:
- `uvx` runs a program in a temporary environment that uv prepares for you;
- `--python 3.14t` asks for the Python that Icaros needs;
- `--from "…whl[ollama]"` says where to get Icaros (the file in `demos/wheels/`), together with what it needs
  to talk to Ollama;
- `icaros demos/icaros-barista/barista.mas2i` starts the multi-agent system;
- `--headless` prints everything in the terminal, with no graphical window.

The first run takes a minute longer, because of the downloads. A successful run looks like this (the
explanation at the end changes every time):

```
agents running: barista (Ctrl-C to stop)
--- I have the steps but not the recipe ---
fetching the beans
grinding
boiling the water
brewing
--- and now let me tell you what I did ---
I made coffee by following these steps in a specific order: ...
```

The lines from `fetching the beans` to `brewing` are printed by the agent's plans: each one appears only
when the LLM asks for that step. The program stops on its own at the end (if it hangs, press `Ctrl-C`).

**If those four lines are missing** and the LLM says something like *"I did not make coffee"*, that is not a
mistake on your side: the small model answered without calling the steps. It happens often with
`qwen3:4b-instruct`. Run the command again, or try a bigger model (see below).

### Shorter command (optional)

To type just `icaros`, install it once:

```bash
uv tool install --python 3.14t "demos/wheels/icaros-0.1.0-py3-none-any.whl[ollama]"
icaros demos/icaros-barista/barista.mas2i --headless
```

If the terminal says `icaros: command not found`, run `uv tool update-shell`, then close the terminal and open a
new one. To remove Icaros: `uv tool uninstall icaros`.

### From the slides

If you started the slides with `uv run slides/serve.py`, the **▶** button on the Icaros slide runs this same
command for you and shows the output in the slide.

## Things to try

Copy the `icaros-barista` folder before changing it (e.g. to `my-barista`), so you can always go back to the
original. Then use your folder in the command, e.g. `icaros demos/my-barista/barista.mas2i --headless`.

1. **Change the model.** In `barista.mas2i`, change the line `model: qwen3:4b-instruct` to another Ollama
   model that supports tool calling, e.g. `model: qwen2.5:7b`. First download it: `ollama pull qwen2.5:7b`.
   Bigger models call the steps much more reliably.

2. **Hide a step from the LLM.** In `barista.mas2i`, the list under `- plans` contains the steps the LLM can
   ask for. Delete the line `- grind` and run again: what does the model do now that it cannot grind the beans?

3. **Write the missing plan yourself, so the agent needs no LLM to make the coffee.** In `barista.asl`:
   - add this line right **above** the line `+!start` (it says: to make a coffee, do these four steps in this
     order):
     ```
     +!make_coffee <- !fetch_beans; !grind; !boil_water; !brew.
     ```
   - inside `+!start`, replace the whole `.run("Make a coffee. … as soon as I believe I have coffee.");`
     statement (it spans several lines: from `.run(` up to the first `");`, included) with:
     ```
     !make_coffee;
     ```

   Run it: the four steps always come out in that order, because now it is the plan that decides, not the
   LLM. The LLM is still used at the end, to write the explanation (that is the `.talk(…)` statement).

4. **See what the LLM receives.** Add `--llm-trace trace.jsonl` at the end of the command. Every request sent
   to the LLM and every answer is saved in `trace.jsonl`, one JSON object per line: you can see how the plans
   of the agent are offered to the model as tools.

5. **Watch the agent in a window.** Use this command instead: it adds the `devui` extra and replaces
   `--headless` with `--ui web`.
   ```bash
   uvx --python 3.14t --from "demos/wheels/icaros-0.1.0-py3-none-any.whl[ollama,devui]" icaros demos/icaros-barista/barista.mas2i --ui web
   ```

## Troubleshooting

| What you see | What to do |
|---|---|
| `uvx: command not found` | uv is not installed: see step 3 of the [setup](../README.md#setup-do-it-before-the-lab) |
| an error about Python `3.14t` (cannot find or download it) | update uv with `uv self update` (older versions do not know Python 3.14t), then try again |
| `Distribution not found at: file:///…/icaros-0.1.0-py3-none-any.whl` or `No such file or directory: 'demos/…/barista.mas2i'` | you are not in the `sdai2026` folder: `cd` into it (it contains `README.md`) |
| a long error ending with `ConnectionError: Failed to connect to Ollama` | Ollama is not running: start the Ollama app (or run `ollama serve` in another terminal) |
| `model "qwen3:4b-instruct" not found` | download it: `ollama pull qwen3:4b-instruct` |
| the four step lines are missing, the LLM says it "did not make coffee" | the model did not call the steps: run again, or use a bigger model (*Things to try* 1) |
