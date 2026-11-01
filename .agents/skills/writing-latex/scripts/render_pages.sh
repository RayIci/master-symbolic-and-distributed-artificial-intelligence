#!/usr/bin/env bash
# Render PDF pages to PNG contact sheets (6 pages per sheet, 3x2) for visual inspection.
# usage: render_pages.sh file.pdf FIRST LAST [outdir] [dpi=70]
set -eu
pdf="$1"; first="$2"; last="$3"; out="${4:-/tmp/latex-pages}"; dpi="${5:-70}"
rm -rf "$out"; mkdir -p "$out"
pdftoppm -r "$dpi" -png -f "$first" -l "$last" "$pdf" "$out/p"
python3 - "$out" <<'PY'
import glob, os, sys
out = sys.argv[1]
files = sorted(glob.glob(os.path.join(out, "p-*.png")))
try:
    from PIL import Image
except ImportError:
    print("Pillow not available; individual pages:"); print("\n".join(files)); sys.exit(0)
for k in range(0, len(files), 6):
    ims = [Image.open(f) for f in files[k:k+6]]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w * 3, h * 2), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 3) * w, (i // 3) * h))
    path = os.path.join(out, f"sheet{k // 6}.png"); sheet.save(path); print(path)
PY
