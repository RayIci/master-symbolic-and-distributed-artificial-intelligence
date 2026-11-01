---
name: writing-latex
description: Write, update, restructure and debug LaTeX documents (notes, course notes, study material, paper explanations, reports) with a clean multi-file structure, a shared preamble of coloured explanation boxes, step-by-step math, TikZ/pgfplots figures and a compile-and-look verification loop. Use this skill whenever the user wants to create or edit .tex files, add a section or chapter to a LaTeX document, turn slides, a PDF, a paper, lecture notes or a topic into LaTeX notes, explain or recap course material in LaTeX, fix LaTeX compile errors or layout problems (overfull boxes, broken figures), or draw plots/diagrams for a LaTeX document — even if they only say "notes", "write it up", "add this to my document" or "rewrite these slides" without mentioning LaTeX explicitly, as long as the project is LaTeX-based.
---

# Writing LaTeX

This skill captures a working method for producing LaTeX documents that are **easy to
study from**: well structured on disk, visually consistent, mathematically careful, and
verified by actually compiling and looking at the pages.

## First: look before you write

1. **Read the project's own rules.** Look for `AGENTS.md` / `CLAUDE.md` in the document
   folder and in every folder you will touch. Project rules override this skill.
2. **Inspect what exists**: the master file (`main.tex`), the preamble, existing sections,
   their labels and macros. Reuse existing macros, colours and boxes; never redefine them.
3. **Check the toolchain** once: `which latexmk pdflatex pygmentize`, and whether Python
   with matplotlib is available if figures may need it.

## Decide which references you need

Read only the files relevant to the task:

| Task involves...                                                    | Read                                |
|----------------------------------------------------------------------|-------------------------------------|
| Creating a document, adding a section, moving/renaming files          | `references/project-structure.md`   |
| Using or setting up the explanation boxes, macros, solutions toggle   | `references/boxes-and-preamble.md`  |
| Explaining material: slides, course PDFs, papers, docs, or a topic from scratch | `references/explanatory-writing.md` |
| Any mathematics: derivations, proofs, worked examples, exercises      | `references/math.md`                |
| Plots, diagrams, 3D surfaces, generated images                        | `references/figures.md`             |
| Compiling, errors, overfull boxes, visual checking                    | `references/build-and-verify.md`    |

For a typical "turn these slides/this paper into notes" task, read
`explanatory-writing.md`, `math.md`, `figures.md` and `build-and-verify.md`.

## Bundled files

- `assets/preamble.tex`: self-contained shared preamble (boxes, colours, macros, plot
  style, solutions toggle). Copy it into a new project as `preamble/preamble.tex`.
- `assets/main-template.tex`: minimal master document that loads the preamble and
  inputs sections.
- `scripts/check_build.sh <main.tex>`: compiles with latexmk and reports errors,
  undefined references and overfull boxes above a threshold, with the source file they
  come from.
- `scripts/render_pages.sh <pdf> <first> <last> [outdir]`: renders pages to PNG
  contact sheets (6 pages per image) so you can *look* at the result with the Read tool.

## The core loop (always)

1. **Plan** the section structure (what sub-sections, which figures, which examples)
   before writing. For large sources, read all of it first so the plan is coherent.
2. **Write** one section at a time, following the structure and box conventions.
3. **Verify numbers** that appear in examples or solutions with a quick script before
   committing them to text.
4. **Compile** after each section (`scripts/check_build.sh`), fix every error and every
   overfull box that is visibly too wide (above ~5pt).
5. **Look at the pages** (`scripts/render_pages.sh`, then Read the contact sheets).
   Overlapping labels, tiny figures, legends showing the wrong line style and equations
   running into the margin only show up visually. Fix and re-render.
6. **Report** what was written, any corrections made to the source material, and
   anything left for the user to decide.

Working section by section matters: a 100-page document with a systematic layout bug
found at the end costs far more to fix than the same bug found after the first section.

## Things that are easy to get wrong

- Long display equations overflow the narrow text block, especially inside boxes. Split
  them with `align*`, one step per line.
- Floats (`figure`) cannot live inside `tcolorbox`; use `center` + `\captionof{figure}`.
- Verbatim/minted cannot go inside environments that collect their body (`\NewEnviron`,
  e.g. the solution box). Put code in normal text or the exercise statement.
- pgfplots trigonometric functions use **degrees** unless `trig format plots=rad`.
- Do not mention repository internals (file paths, script names, macro names, "generated
  by ...") in the text the reader sees; the PDF is for studying, not for maintaining.
- When moving files, use `git mv` if the project is a git repo, then fix every `\input`,
  `\includegraphics` and `\inputminted` path, rebuild from clean (`latexmk -C`), and
  grep the PDF text for leftovers.
