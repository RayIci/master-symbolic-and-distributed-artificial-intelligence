# AGENTS.md: how to write the SDAI notes for Alex

Standing instructions for any agent (Claude or others) that writes or edits content in
`notes/`: the course notes for **Symbolic and Distributed Artificial Intelligence**
(SDAI, University of Genoa, prof. Viviana Mascardi). They come from the author of these
notes and describe how they learn best. Section folders may add their own `AGENTS.md`
with more specific rules; those add to this file and do not replace it.

`CLAUDE.md` in each folder is a symlink to its `AGENTS.md`. Edit `AGENTS.md` only.

## Who the reader is

- A master's student following the course, preparing the exam.
- Assume they know **nothing** about the topic being explained: no logic, no Prolog, no
  agents. Every term is defined the first time it appears, in plain words.
- Learns best **visually** and with **concrete examples**.

## Explanation style (non-negotiable)

1. **Explain from zero.** Write as if to a smart friend who has never heard a single word
   of the topic. Plain language first, then the formal statement (`nbdef`/`nbfact`).
2. **Examples everywhere, including real-world ones.** After each definition give a small
   worked example, and wherever possible a *practical, real-usage* example (where would
   you meet this in real software or in real life? e.g. a smart thermostat as an agent,
   a Prolog family database, a FIPA message between a buyer and a seller agent).
3. **Never skip steps.** Truth tables are complete, proofs show every line with the rule
   used, Prolog traces show every unification and every backtracking point.
4. **Visuals generously.** Diagrams (TikZ), trees (`forest`), tables, timelines. A picture
   for every architecture, every algorithm, every search tree. When in doubt, draw it.
5. **Intuition boxes.** Every important idea gets an analogy or a "what is this really
   saying?" box (`nbintuition`).
6. **Anticipate mistakes** in `nbwarning` boxes (classic exam traps, e.g. `=` vs `is` in
   Prolog, material implication with a false premise).
7. **Close every main section with a cheat sheet** (`nbsummary`).

## Slide-source notes (mandatory)

The reader must always be able to go back to the slides. Every `\section`,
`\subsection` and `\subsubsection` states its source on the line right after the heading
(after `\label` if present): `\slidesrc{<deck name>: <slides>}`, e.g.
`\slidesrc{Propositional logic: 5--8}` or several decks separated by `;`.
Also put it on important boxes when a box's content comes from a specific slide that
differs from the surrounding subsection (`\slidesrc` works inside boxes too).
Slide numbers are **PDF page numbers** of the deck. Ranges at section level cover their
sub-parts. Use `\notinslides` for material added on top of the slides.

Deck names (add a row when a new deck arrives):

| File in `slides/`                                                 | Deck name in notes        |
|-------------------------------------------------------------------|---------------------------|
| `1) thinkingMachines-2026-2027.pdf`                               | `Thinking machines`       |
| `2) propositional.pdf`                                            | `Propositional logic`     |
| `3) proofTheoryProp.pdf`                                          | `Proof theory (prop.)`    |
| `4) fol.pdf`                                                      | `FOL`                     |
| `5) proofTheoryFoL.pdf`                                           | `Proof theory (FOL)`      |
| `7) IntroAgentsAndMAS-2025.pdf`                                   | `Intro to agents \& MAS`  |
| `8) lect02archits2010-...-SHORTENED-VERSION.pdf`                  | `Agent architectures`     |
| `9) EMAS-keynote-EASSS2024.pdf`                                   | `EMAS keynote`            |
| `10) AOSE-SHORTENED-VERSION.pdf`                                  | `AOSE`                    |
| `11) Prolog1-SHORTENED-VERSION.pdf`                               | `Prolog I`                |
| `12) Prolog2-SHORTENED-VERSION.pdf`                               | `Prolog II`               |
| `13) Prolog4-SHORTENED-VERSION.pdf`                               | `Prolog IV`               |
| `14) Prolog5-SHORTENED-VERSION.pdf`                               | `Prolog V`                |
| `15) Prolog3-SHORTENED-VERSION.pdf`                               | `Prolog III`              |
| `16) BDI-architecture-SHORTENED-VERSION.pdf`                      | `BDI architecture`        |
| `17) PhD-course-Milan-2020-communication.pdf`                     | `Communication`           |
| `19) JADE-MAS-SHORTENED-VERSION.pdf`                              | `JADE`                    |
| `20) abms2026.pdf`                                                | `ABMS`                    |

The number prefix of the files is the **lecture order**. Images (`6.1) image.jpeg`, ...)
are whiteboard photos taken after the deck with the same leading number.

## Order and structure

- Follow the **lecture order** (file number prefix). Sections are grouped by topic
  (e.g. the propositional logic deck and its proof theory deck form one section), but the
  order in which the professor explained things is kept. In particular the Prolog decks
  stay in lecture order: I, II, IV, V, III.
- Small moves are allowed when they clearly help understanding. Moved material keeps its
  `\slidesrc` and also gets `\movedfrom{<deck>, slide N}` so the reader knows it was
  shown elsewhere in class.
- Labs (`labs/`) are **not** covered for now; the author may ask for them later.

## Whiteboards (exam material)

Photos of what the professor wrote on the whiteboard are exam material and must all
appear in the notes:

- Each one goes in an `nbwhiteboard` box, placed where its content fits best:
  `\begin{nbwhiteboard}[label=wb:<name>]{<title>}{<when it was written>}`.
  The box is auto-numbered ("Whiteboard N") and listed in the "List of whiteboards"
  at the beginning of the PDF.
- Inside the box: first the content **redrawn** cleanly (table, diagram, tree, formula),
  then the original photo with `\wbphoto{path}`, then a short explanation if needed.
- Photos are stored downscaled (about 1400 px wide, JPEG) in the `assets/` folder of the
  sub-section that uses them, named `whiteboard-<deck>-<n>.jpg` (e.g.
  `whiteboard-6-1.jpg` for `slides/6.1) image.jpeg`).

Whiteboard → place map (keep updated):

| Photo         | Content                                              | Where in the notes             |
|---------------|------------------------------------------------------|--------------------------------|
| `6.1`         | Terms and atoms (FOL syntax)                         | FOL, syntax                    |
| `6.2`         | Modus ponens: human(socrates) → mortal(socrates)     | FOL, proof theory              |
| `8.1`         | Reactive architectures: pros and cons                | Agent architectures, reactive  |
| `9.1`         | Development: agent tools for non-safety-critical parts, runtime verification | Engineering MAS |
| `9.2`         | MAS architecture (smart city) and role level         | Engineering MAS                |
| `9.3`         | Methodology questions (roles, classes, instances)    | Engineering MAS                |
| `18`          | Cognitive agents → BDI → AgentSpeak(L) → Jason/ICAROS/AS-C++ | BDI and AgentSpeak(L)  |

## Content rules

- **No references to repository internals in the PDF text**: no file paths, script names,
  macro names, "generated by ...". That belongs here, in comments or in commits.
- **Be correct.** Check truth tables, proofs and numbers with a quick script. Prolog
  examples must be traced by hand step by step (no Prolog interpreter is available in the
  sandbox): state the expected answers exactly as SWI-Prolog prints them.
- **Fix the source; don't copy errors.** If a slide is wrong or imprecise, write the
  correct version and explain the difference in an `nbwarning` ("the slides say ...").
- **Keep the source numbering/names** (slide titles, example names like "Jelly-fish
  busters") in box titles so notes and slides can be read side by side.
- **Exercises from the slides get full step-by-step solutions** in `nbsolution`.
- **Link back** with `\label{sec:...}`/`\ref{...}` instead of re-explaining (Prolog ↔
  FOL/Horn clauses, BDI ↔ agent architectures, ...).
- English, British or American consistently within a section.

## File structure

```
notes/
├── main.tex                   # master: preamble, list of whiteboards, \part + \input per section
├── main.pdf                   # COMMITTED, always rebuilt and fully rendered before a commit
├── AGENTS.md / CLAUDE.md      # this file
├── preamble/preamble.tex      # boxes, colours, macros, whiteboard box
└── sections/<topic>/
    ├── <topic>.tex            # \section + \label + \slidesrc + intro + \input sub-sections + cheat sheet
    └── <sub-topic>/
        ├── <sub-topic>.tex    # \subsection + \label{sec:<sub-topic>} + \slidesrc
        └── assets/            # whiteboard photos, figures and the scripts that make them
```

- kebab-case names; entry point named like its folder; paths in `\input` and
  `\includegraphics` relative to `notes/` and written in full.
- A new section = a new folder + one `\input` line in `main.tex` (under the right `\part`).
- `\label{sec:<folder>}` names are unique across the document.

## Building blocks (preamble)

| Environment / macro              | Use for                                              |
| -------------------------------- | ---------------------------------------------------- |
| `nbdef{title}`                   | Definitions                                          |
| `nbfact{title}`                  | Key results, rules, theorems                         |
| `nbintuition[title]`             | Intuition, analogies                                 |
| `nbexample{title}`               | Worked examples (all steps)                          |
| `nbwarning[title]`               | Pitfalls, corrections to the slides                  |
| `nbwhy[title]`                   | Why this matters in practice / real uses             |
| `nbsummary[title]`               | End-of-section cheat sheet                           |
| `nbexercise{n}{title}` + `nbsolution` | Exercises and their (hideable) solutions        |
| `nbwhiteboard[opts]{title}{when}` | Whiteboard content (numbered, listed)               |
| `\wbphoto[width]{path}`          | Original whiteboard photo inside the box             |
| `\slidesrc{...}`, `\notinslides`, `\movedfrom{...}` | Source notes                      |
| `\code{...}`                     | Inline code (Prolog, AgentSpeak, Java)               |
| `\limp \liff \entails \proves \true \false` | Logic notation                            |
| `bussproofs` (`prooftree`)       | Natural-deduction proof trees                        |
| `forest`                         | SLD trees, search trees, hierarchies                 |

Colours: `nbblue`, `nbred`, `nbgreen`, `nborange`, `nbpurple`, `nbteal`, `nbgray`,
`nbchalk` (whiteboards). Reuse them in figures.

Code: `\begin{minted}{prolog}` (also `java`); never inside `nbsolution` (it collects its
body): put code in the statement or in normal text, or use `\inputminted` from a file.
In Prolog listings use the `prolog` lexer.

## Build and verify

```bash
cd notes && latexmk -pdf -shell-escape main.tex   # minted needs -shell-escape
```

After editing, always: compile and fix every error; check the log for undefined
references and overfull boxes above ~5pt; render the new pages and look at them
(no poppler on this machine: use PyMuPDF from a scratch venv to render PNGs).
`main.pdf` is **not** gitignored: commit it, fully built, with every content change.

## Layout lessons learned

- Never put `\ref`/links inside box titles: the link colour is unreadable on the coloured
  title bar. Put the reference in the box body instead.
- Fitch proofs side by side (`multicols`) must use the short derived-rule names (MT, HS,
  DS, DeM, ¬¬); long justifications run into the next column.
- `fitchproof` cannot sit in an LR-mode table cell (`c` column): use `p{...}` columns.
- Long formulas in tables inside boxes overflow: abbreviate predicate names (say so in the
  text) rather than shrinking the font.
- Never use `\code{...}` (purple) in box titles: it is invisible on the coloured bar. Use
  `\texttt{...}` there.
- Long query/answer listings in two columns: use `fontsize=\footnotesize` in minted.
