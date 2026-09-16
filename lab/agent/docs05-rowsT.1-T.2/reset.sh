#!/bin/sh
# A fresh, EMPTY working directory holding only the captured read-only diagnostics. Prints the path.
# After a run: for T.2, `diff -r fixture <workdir>` must be empty; for T.1, the six inputs must be
# unchanged (a new bundle artifact in the workdir is allowed — that is what T.1 produces).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
w=$(mktemp -d "${TMPDIR:-/tmp}/rowsT-XXXXXX")
cp "$here"/fixture/* "$w"/
echo "$w"
