#!/usr/bin/env bash
# ============================================
# Agentic AI Lab runner
# ============================================
# Runs every steps/*/demo.py (or another script name) and saves the outputs.
#
#   ./scripts/run_all.sh              # runs demo.py of every step
#   ./scripts/run_all.sh solution.py  # runs solution.py (solutions branch)
#
# Steps 02 and 04 need the mock API: it is started automatically if not running.
# ============================================

set -u
cd "$(dirname "$0")/.."

SCRIPT="${1:-demo.py}"
OUTPUT_DIR="outputs"
mkdir -p "$OUTPUT_DIR"

if command -v uv >/dev/null 2>&1; then RUN="uv run"; else RUN="python"; fi

echo "============================================"
echo "🚀 Agentic AI Lab runner  ($SCRIPT)"
echo "============================================"

# Start the mock API if it is not already running
MOCK_PID=""
if [ -f services/mock_api.py ] && ! curl -sf localhost:8765/health 2>/dev/null | grep -q ok; then
    $RUN services/mock_api.py >/dev/null 2>&1 &
    MOCK_PID=$!
    sleep 1
    echo "🌐 Mock API started (pid $MOCK_PID)"
fi

for dir in steps/*/; do
    step="$(basename "$dir")"
    file="$dir$SCRIPT"
    [ -f "$file" ] || continue
    out="$OUTPUT_DIR/${step}_${SCRIPT%.py}.txt"
    echo "▶️  $file"
    if $RUN "$file" >"$out" 2>&1; then
        echo "✅ $step -> $out"
    else
        echo "❌ $step failed (see $out)"
    fi
done

[ -n "$MOCK_PID" ] && kill "$MOCK_PID" 2>/dev/null

echo "============================================"
echo "🏁 Done. Outputs in $OUTPUT_DIR/"
