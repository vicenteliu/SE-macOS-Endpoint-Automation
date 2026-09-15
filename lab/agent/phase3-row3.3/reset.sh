#!/bin/sh
# Return the phase-3 lab to the state before any Praat run: no override, no cache, no repo item,
# parent recipe as checked out. Run between models so every model starts from the same place.
set -eu
REPO=/Users/Shared/munki_repo
RECIPES=~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes
rm -f ~/Library/AutoPkg/RecipeOverrides/Praat.munki.recipe
rm -rf ~/Library/AutoPkg/Cache/local.munki.Praat
rm -f "$REPO"/pkgsinfo/apps/Praat-*.plist "$REPO"/pkgs/apps/Praat-*.dmg "$REPO"/pkgs/apps/Praat-*.zip "$REPO"/icons/Praat.png
git -C "$RECIPES" checkout -- Praat/Praat.download.recipe Praat/Praat.munki.recipe
makecatalogs "$REPO" >/dev/null
echo "reset: override, cache, repo item and parent recipe restored"
