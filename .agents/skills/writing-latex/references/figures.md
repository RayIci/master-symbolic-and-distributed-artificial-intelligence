# Figures

## Choosing the tool

- **TikZ / pgfplots** (default): vector graphics with the document's fonts, compiled with
  the document, easy to tweak. Diagrams, geometry, 2D function plots, bar charts,
  moderate 3D surfaces.
- **Python / matplotlib**: when it is clearly cleaner, e.g. 3D surfaces with overlaid
  fields, images with quiver plots, simulations (random walks, law of large numbers),
  histograms of real data. Save the script and its PDF output in the section's
  `assets/`, commit both, seed all randomness, and `\includegraphics[width=\linewidth]`.
  If matplotlib is not installed, create a venv in a scratch directory rather than
  installing into the user's environment.

## Placing figures

```latex
\begin{center}
\begin{tikzpicture} ... \end{tikzpicture}
\captionof{figure}{What to notice: the eigenvectors are the axes of the ellipse.}
\end{center}
```

- `center` + `\captionof` works inside boxes (floats do not) and keeps the figure next
  to the text it explains.
- Captions say **what to see**, not just what is drawn.

## TikZ patterns that worked

- 2D vectors: `\draw[-{Stealth}, very thick, nbblue] (0,0) -- (3,1) node[right] {$\vect u$};`
- Angles: `\pic[draw, angle radius=0.8cm, "$\theta$", angle eccentricity=1.4] {angle = B--O--A};`
  (needs the `angles` and `quotes` libraries).
- Braces: `decorations.pathreplacing` with `decoration={brace, amplitude=4pt}`.
- Linear maps on a grid: draw the grid inside `\begin{scope}[cm={a,c,b,d,(0,0)}]` to show
  how a matrix deforms the plane (columns = images of the basis vectors).
- Cheap 3D without extra packages:
  `\begin{tikzpicture}[x={(-0.55cm,-0.4cm)}, y={(1cm,0cm)}, z={(0cm,1cm)}]` and 3-coordinate points.
- Regular polygons: `\draw (0:1) \foreach \k in {1,...,7} { -- (\k*45:1) } -- cycle;`
- Computation graphs / pipelines: nodes with `positioning` (`right=of a`), forward arrows
  above, backward arrows below with `bend left` and labels.

## pgfplots gotchas

- **Trig in degrees by default.** The shared `nbplot` style sets
  `trig format plots=rad`; set it yourself on any axis that does not use `nbplot`.
- **Legends follow plot order**, not `\addlegendentry` placement. Add `forget plot` to
  helper plots (the line `y = x`, fills, marker-only plots) or the legend shows the
  wrong styles.
- **`coordinates {...}` does not evaluate expressions** reliably. Compute the numbers
  first (in your head or a script) and write literals.
- Avoid `\foreach` with macros inside `axis` unless you `\edef` the plot command; often
  writing three explicit `\addplot` lines is simpler and safer.
- Titles and the top y-axis label collide with `axis lines=middle`; `nbplot` shifts the
  title up. Remove `ylabel` in small group plots if it still collides.
- Asymptotes: `restrict y to domain=-3:3, unbounded coords=jump, samples=600` for tan-like
  functions.
- Areas: `\usepgfplotslibrary{fillbetween}`, name the paths, then
  `\addplot[fill] fill between[of=f and ax, soft clip={domain=a:b}];`.
- Several panels: `groupplots` with `group style={group size=3 by 1, horizontal sep=0.9cm}`.
  Check the total width fits the text block.
- 3D: `\addplot3[surf, shader=interp]` with `samples=21..25`; more is slow.

## Visual quality checklist

After compiling, render the pages (see `build-and-verify.md`) and check:
- labels do not overlap curves, arrows or each other;
- the figure is big enough to read (scale it up if text in it is smaller than footnote size);
- the figure does not run past the margin (panels side by side are the usual culprit);
- legend line styles match the curves;
- colours are consistent with the box colours and with other figures in the document.
