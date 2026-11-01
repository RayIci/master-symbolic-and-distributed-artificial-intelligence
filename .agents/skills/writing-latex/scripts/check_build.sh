#!/usr/bin/env bash
# Compile a LaTeX document with latexmk and summarise problems in the log.
# usage: check_build.sh path/to/main.tex [overfull_threshold_pt=5]
set -u
main="$1"; thr="${2:-5}"
dir="$(cd "$(dirname "$main")" && pwd)"; base="$(basename "$main" .tex)"
cd "$dir" || exit 1
latexmk -pdf -shell-escape -interaction=nonstopmode "$base.tex" > /dev/null 2>&1
log="$base.log"
[ -f "$log" ] || { echo "no log produced"; exit 1; }
python3 - "$log" "$thr" <<'PY'
import re, sys
log, thr = sys.argv[1], float(sys.argv[2])
text = open(log, errors="replace").read()
# track which file is open: '(./path.tex' pushes, ')' pops (approximation)
stack, current = [], {}
errors, refs, overfull = [], set(), []
lines = text.splitlines()
for i, line in enumerate(lines):
    for m in re.finditer(r"\((\./[^\s()]+\.tex)|\)", line):
        if m.group(1): stack.append(m.group(1))
        elif stack: stack.pop()
    where = stack[-1] if stack else "?"
    if line.startswith("!"):
        errors.append(f"{where}: {line}  {' '.join(lines[i+1:i+3])}")
    m = re.search(r"Reference `([^']+)' on page (\d+) undefined", line)
    if m: refs.add(m.group(1))
    m = re.search(r"Overfull \\hbox \(([\d.]+)pt too wide\).*?lines? ([\d-]+)", line)
    if m and float(m.group(1)) > thr:
        overfull.append(f"{where}: {m.group(1)}pt at line {m.group(2)}")
pages = re.search(r"Output written on .*?\((\d+) pages?", text)
print(f"pages: {pages.group(1) if pages else '?'}")
print(f"errors: {len(errors)}"); [print("  " + e) for e in errors[:20]]
print(f"undefined refs: {len(refs)}"); [print("  " + r) for r in sorted(refs)]
print(f"overfull > {thr}pt: {len(overfull)}"); [print("  " + o) for o in overfull]
print("note: overfull line numbers often point at the END of an environment; render the page to locate it.")
PY
