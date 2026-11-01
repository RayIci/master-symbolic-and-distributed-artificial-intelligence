# Boxes and the shared preamble

`assets/preamble.tex` defines a small, fixed vocabulary of coloured boxes. Fixed meanings
let a reader scan a page and immediately know what kind of content each block is.
Copy it to `preamble/preamble.tex` and `\input{preamble/preamble}` from `main.tex`. It
loads the packages it needs itself (loading a package twice without options is harmless).

If the project already has a preamble with boxes (possibly with another prefix), use
that one instead and follow its names. Do not mix two box systems in one document.

## The boxes

| Environment                    | Colour  | Use for                                                      |
|--------------------------------|---------|--------------------------------------------------------------|
| `nbdef{title}`                 | blue    | Definitions: the precise formal statement                   |
| `nbfact{title}`                | green   | Theorems, facts, key results, important formulas            |
| `nbintuition[title]`           | orange  | Intuition, analogies, pictures, "what is this really saying" |
| `nbexample{title}`             | purple  | Worked examples with every step                              |
| `nbwarning[title]`             | red     | Pitfalls, misconceptions, corrections to the source          |
| `nbwhy[title]`                 | teal    | Why this matters / applications in the reader's field       |
| `nbsummary[title]`             | gray    | Cheat sheet at the end of a section                          |
| `nbexercise{number}{title}`    | black   | Exercise statement                                           |
| `nbsolution`                   | green   | Solution, hidden globally with `\showsolutionsfalse`         |

Box titles render as "Definition --- <title>"; square-bracket titles are optional.
`nbwhy` defaults to the title "Why this matters"; change it per project with
`\renewcommand{\nbwhytitle}{Why this matters for DSP \& ML}` in the preamble.

Guidelines:
- One idea per box. A box that runs for two pages has stopped being a highlight.
- Not everything goes in a box: connective prose, derivations and proofs usually sit
  between boxes. Put the *statement* in `nbfact`, the *proof* right after it.
- Keep the source numbering in titles when working from course material:
  `\begin{nbdef}{Linear span (Def.~1.4)}`.
- Boxes nest (e.g. an intuition box inside a solution), but keep nesting to one level.
- Inside boxes there are no floats: use `\begin{center}...\captionof{figure}{...}\end{center}`.

## The solutions toggle

`nbsolution` is built with `\NewEnviron`: when `\showsolutionsfalse` is set, the whole
body is dropped. Consequences:
- The reader (or the user) can print an exercise-only version by flipping one line.
- Verbatim material (`minted`, `verbatim`, `lstlisting`) cannot be used inside it. Put
  code in the exercise statement or in normal text; `\inputminted` from a file is the
  cleanest option.

## Macros

`\reason{...}` adds a short grey justification at the end of an equation line
(`\qquad ◁ text`); see `math.md`. Notation macros (`\vect`, `\ip`, `\norm`, `\abs`, `\T`,
`\R`, `\C`, `\E`, `\Prob`, `\Var`, `\tr`, `\dd`, `\col`, ...) are listed in the preamble.
Use them consistently instead of typing raw notation, so a later change of notation is a
one-line edit.

## Colours

`nbblue`, `nbred`, `nbgreen`, `nborange`, `nbpurple`, `nbteal`, `nbgray`. Use them in
figures too, so plots match the boxes and the document looks like one system. A common
convention: blue/red for the two main objects, purple for their combination, green for
results/regions, orange for annotations, gray for helper lines.
