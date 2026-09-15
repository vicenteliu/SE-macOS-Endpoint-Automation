#!/bin/sh
# Simulate an upstream change to the parent recipe AFTER an override pinned it: one XML comment.
# The override's ParentRecipeTrustInfo no longer matches, so `autopkg run` must refuse.
set -eu
F=~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Praat/Praat.download.recipe
grep -q "lab: simulated upstream change" "$F" && { echo "induce: already applied"; exit 0; }
sed -i '' 's#<plist version="1.0">#<plist version="1.0"><!-- lab: simulated upstream change -->#' "$F"
autopkg verify-trust-info Praat.munki 2>&1 | tail -2 || true
echo "induce: parent recipe changed; trust info for the override should now fail"
