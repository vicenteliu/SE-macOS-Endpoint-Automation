#!/bin/sh
# Give a model a fresh, EMPTY working directory holding only the two exports. Prints the path.
# After the run: `diff -r fixture <workdir>` tells you whether the model changed a file.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
w=$(mktemp -d "${TMPDIR:-/tmp}/rowI.1-XXXXXX")
cp "$here"/fixture/*.csv "$w"/
echo "$w"
