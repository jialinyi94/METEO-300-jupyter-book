#!/usr/bin/env bash
# Run ruff on the code cells of MyST Markdown notebooks.
# jupytext converts each page to a Python script on stdout; the page file stays unchanged.
# Usage: tools/ruff_md.sh docs/topics/ch03-pressure-hydrostatic.md [...]
set -uo pipefail
rc=0
for f in "$@"; do
  grep -q '{code-cell}' "$f" || continue
  jupytext --quiet --to py:percent -o - "$f" \
    | ruff check --quiet --stdin-filename "${f%.md}.py" - || rc=1
done
exit $rc
