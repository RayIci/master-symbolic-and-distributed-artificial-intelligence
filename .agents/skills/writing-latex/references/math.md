# Writing mathematics

## Step-by-step derivations

Use `align*` with one transformation per line and a short justification on the right:

```latex
\begin{align*}
  \norm{\vect u + \vect v}^2 &= \ip{\vect u + \vect v}{\vect u + \vect v} \reason{definition of norm} \\
  &= \norm{\vect u}^2 + 2\ip{\vect u}{\vect v} + \norm{\vect v}^2 \reason{bilinearity, symmetry} \\
  &\le \norm{\vect u}^2 + 2\norm{\vect u}\norm{\vect v} + \norm{\vect v}^2 \reason{Cauchy--Schwarz}
\end{align*}
```

- One rule per line. If two things happen at once (expand *and* cancel), either split the
  line or name both in the reason.
- Keep `\reason{}` to a few words (`linearity`, `$i^2 = -1$`, `FTC`). Longer explanations
  go in the text before or after the display; long reasons are the most common cause
  of overfull lines.
- When a step uses a fact proved elsewhere, cite it: `\reason{Fact~2.2}`.
- End proofs with `\hfill$\square$` or `\tag*{$\square$}` on the last aligned line.

## Fitting the page

The text block is often narrow (and narrower inside boxes), so:
- Never put a long chain `a = b = c = d = e` in one `\[ \]`. Break it in `align*`.
- At most two short equations side by side; otherwise stack them.
- Break a long left-hand side onto its own line:
  ```latex
  &\frac{f(x+h)g(x+h) - f(x)g(x)}{h} \\
  &\quad= \dots
  ```
- Prefer `\tfrac` for small inline fractions inside long lines.
- After compiling, treat any overfull box above ~5pt as a bug (see `build-and-verify.md`).

## Explaining a formula

For each important formula, answer in prose: what each symbol is, the domain/shape of
each object (scalar? vector of size n? matrix m×n?), why each hypothesis is needed, and
what the formula looks like in a tiny case (n = 2, concrete numbers). Shapes deserve
special attention in linear algebra: state them whenever a product appears.

## Worked examples and exercises

- Start from the given data, write the equation to solve, and solve it fully.
- When solving systems, show the elimination (which equation minus which).
- When computing matrices entry by entry, show at least one entry in full
  ("row 1 · column 2 = 1·1 + 2·(−1) + 0·2 = −1").
- **Verify before writing**: run the numbers in Python (numpy for linear algebra,
  `fractions.Fraction` for exact probability tables, numerical integration or finite
  differences for calculus). Signs of eigenvectors/singular vectors are arbitrary, so
  compare up to sign.
- **End with a check** visible to the reader: substitute back, rebuild the matrix
  (`QΛQᵀ = A`), compare with an alternative method, or use an invariant (trace = sum of
  eigenvalues, det = product, probabilities sum to 1, Frobenius norm² = Σσ²).

## Correctness traps met in practice

- Angle between vectors: arccos returns values in [0, π].
- Phase of a complex number: `arctan(b/a)` only for a > 0; add π when a < 0.
- SVD: compute V from AᵀA, then *define* `u_i = A v_i / σ_i` so the signs of U and V match.
- `tr(AB) = tr(BA)` only when both products are square.
- Exact vs approximate: if a statement only holds to first order (e.g. using
  `1 + u ≈ e^u`), say so, give the approximation, and state the exact result too.
- A "proof" that silently assumes the conclusion (e.g. assumes eigenvalues are real while
  proving they are real) should be replaced by a correct one.
- Inequality constraints in optimisation: check interior critical points *and* the
  boundary.

## Notation discipline

- Use the preamble macros (`\vect`, `\ip`, `\norm`, `\T`, `\E`, `\Var`, `\dd`, `\col`, ...).
- Pick one convention per document and state it once: matrix sizes (A ∈ ℝ^{m×n}),
  bold vectors, calligraphic maps vs upright matrices, `i` vs `j` for the imaginary unit.
  If the source uses another convention, say which one you use and why.
- Add new general macros to the preamble, never locally in a section.
