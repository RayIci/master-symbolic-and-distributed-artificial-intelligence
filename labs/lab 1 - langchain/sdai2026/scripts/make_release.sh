#!/usr/bin/env bash
# ============================================
# For teachers: build the files to upload on the course page
# ============================================
#   ./scripts/make_release.sh lab         -> dist/sdai2026-lab.zip
#        the git repository with the `main` branch and the step-* tags only (NO solutions);
#        also tags locally what was released (`released-lab`)
#   ./scripts/make_release.sh solutions   -> dist/sdai2026-solutions.bundle + dist/sdai2026-solutions.zip
#        the `solutions` branch as a git bundle (students `git fetch` it into their copy, keeping
#        their work) and, for those who do not use git, the whole repository on `solutions`
#
# Run it from the teacher's copy of the repository (the one that has the `solutions` branch).
# After the lab zip has been distributed, do NOT rewrite main's history: add commits on top
# (and `git merge main` into solutions), otherwise the bundle no longer fits the students' copy.
# ============================================

set -euo pipefail
cd "$(dirname "$0")/.."
REPO="$PWD"
DIST="$REPO/dist"
NAME="sdai2026"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$DIST"

if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  uncommitted changes: they will NOT be in the release (only committed work is packaged)"
fi

# clone <branch> [<extra branch>]: a fresh copy with only those branches and the step tags
clone() {
    # --no-local: a local clone would hardlink the WHOLE object store, solutions included (recoverable
    # with git cat-file even if unreachable); this way only the objects of the cloned refs are copied
    git clone --quiet --no-local --no-tags --single-branch --branch "$1" "$REPO" "$WORK/$NAME"
    if [ $# -gt 1 ]; then
        git -C "$WORK/$NAME" fetch --quiet origin "refs/heads/$2:refs/heads/$2"
    fi
    for tag in $(git tag -l 'step-*'); do
        git -C "$WORK/$NAME" fetch --quiet origin "refs/tags/$tag:refs/tags/$tag"
    done
    git -C "$WORK/$NAME" remote remove origin   # it would point to the teacher's disk
}

case "${1:-}" in
    lab)
        clone main
        rm -f "$DIST/$NAME-lab.zip"
        (cd "$WORK" && zip -qr "$DIST/$NAME-lab.zip" "$NAME")
        echo "✅ $DIST/$NAME-lab.zip  (branches: $(git -C "$WORK/$NAME" branch --format='%(refname:short)' | tr '\n' ' '))"
        # remember what the students received: the solutions bundle is built on top of it
        git tag -f released-lab main >/dev/null
        echo "   (local tag 'released-lab' -> $(git rev-parse --short main), not included in the zip)"
        ;;
    solutions)
        git rev-parse --verify --quiet solutions >/dev/null || { echo "❌ no 'solutions' branch here"; exit 1; }
        # only the commits the students do not have yet: everything after the released lab
        BASE=released-lab
        git rev-parse --verify --quiet "$BASE" >/dev/null || { BASE=main; echo "⚠️  no 'released-lab' tag (run '$0 lab' first): using main as base"; }
        git bundle create "$DIST/$NAME-solutions.bundle" solutions "^$BASE"
        clone solutions main
        rm -f "$DIST/$NAME-solutions.zip"
        (cd "$WORK" && zip -qr "$DIST/$NAME-solutions.zip" "$NAME")
        echo "✅ $DIST/$NAME-solutions.bundle"
        echo "✅ $DIST/$NAME-solutions.zip"
        ;;
    *)
        echo "usage: $0 lab|solutions"
        exit 1
        ;;
esac
