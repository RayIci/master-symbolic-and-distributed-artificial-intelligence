# Build and verify

## Compile

```bash
cd <folder of main.tex>
latexmk -pdf -shell-escape -interaction=nonstopmode main.tex
```
`-shell-escape` is needed by `minted` (which also needs `pygmentize`). Or use
`scripts/check_build.sh main.tex`, which compiles and summarises the log.

## Read the log

- **Errors** (`^!` lines): fix all of them. With `-interaction=nonstopmode` latexmk may
  still produce a PDF, so do not trust the exit code alone.
- **Undefined references**: a `\ref` to a label that does not exist yet. Create a
  placeholder entry file with the label, or fix the name.
- **Overfull \hbox**: content wider than the line. Above ~5pt it is visible. The
  reported line number is often the *end* of an environment (`\end{align*}`, or the end of
  a solution box, since `\NewEnviron` bodies are typeset at the end), so locate the
  problem by rendering the page rather than trusting the line number.
  `check_build.sh` prints the file each warning comes from.
- Typical fixes: split the equation (see `math.md`), shorten `\reason{}`, scale a figure,
  make a long path breakable with `\nolinkurl{}` (from hyperref) instead of `\texttt{}`.

## Look at the pages

Errors in the log are only half the story. Render and inspect:

```bash
scripts/render_pages.sh main.pdf 37 54            # writes sheet0.png, sheet1.png, ... (6 pages each)
```
then open the sheets with the Read tool. Find page numbers for a section in `main.toc`
(`\contentsline {subsection}{...}{<page>}`) or with
`pdftotext -f N -l N main.pdf - | grep "Section title"`.

Look for: equations running into the margin, overlapping figure labels, figures that are
too small, legends with wrong styles, boxes that start at the bottom of a page with one
line, and anything that looks inconsistent with the rest of the document.

## Final checks before handing over

- Clean rebuild after structural changes: `latexmk -C main.tex && rm -rf _minted*`.
- `pdftotext main.pdf - | grep -nE "\.py|\.tex|assets/|Generated"` should find nothing
  in the reader-facing text (code listings that are part of the material excepted).
- Report remaining small warnings honestly (e.g. "four overfull boxes under 6pt, not
  visible") rather than claiming a clean build.
- Do not commit unless asked. Auxiliary files (`*.aux`, `*.log`, `*.fdb_latexmk`,
  `_minted*`) should be gitignored.
