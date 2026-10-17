#!/usr/bin/env bash
# Run ruff on the code cells of MyST Markdown notebooks.
# jupytext converts each page to an .ipynb notebook on stdout; the page file stays unchanged.
# ruff reads notebooks natively, so it checks only the code cells and reports "cell N:line".
# Usage: tools/ruff_md.sh docs/topics/ch03-pressure-hydrostatic.md [...]
set -uo pipefail
rc=0
for f in "$@"; do
  grep -q '{code-cell}' "$f" || continue
  jupytext --quiet --to ipynb -o - "$f" \
    | ruff check --quiet --stdin-filename "${f%.md}.ipynb" - || rc=1
done
exit $rc
