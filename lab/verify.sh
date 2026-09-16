#!/bin/bash
# lab/verify.sh — the read-only verification pass for phases 1, 2 and 3, run on a real Mac.
#
# Every command here reads; none changes anything. Its purpose (TODO item 4) is that the expected
# output in this repository is an output that was *seen* on a real machine — including the
# unglamorous ones. The machine this was captured on is UNMANAGED (no DEP, no MDM), so the
# enrolment and profile rows answer "No" and "none", honestly, and the FileVault row shows a
# Personal Recovery key rather than an MDM bootstrap token. That is the point: an unmanaged
# machine is a real machine, and "not enrolled" is a real expected output.
#
# Phases 4, 5 and 6 are not here: nothing in them can be verified from one machine (docs/04).
# Phase 3's rows need the munki repo reachable — set MUNKI_REPO_URL if it is not the default.
#
# Run:  bash lab/verify.sh | tee lab/verify.out
set -u
REPO_URL="${MUNKI_REPO_URL:-http://localhost/munki_repo}"
sec(){ printf '\n===== %s =====\n' "$*"; }
row(){ printf '\n[%s] %s\n' "$1" "$2"; }
run(){ printf '  $ %s\n' "$1"; eval "$1" 2>&1 | sed 's/^/  /'; }

sec "the machine (management state decides how every row below reads)"
run "sw_vers"

sec "Phase 1 — enrolment"
row 1.2 "how the machine enrolled — or that it did not"
run "profiles status -type enrollment"
row 1.4 "volume ownership, and the recovery path the machine actually has"
run "fdesetup status"
run "diskutil apfs listCryptoUsers /"

sec "Phase 2 — configuration"
row 2.1 "the configuration profiles the machine actually carries"
run "profiles list"
printf '  # system scope needs root: sudo profiles list ; a byte-for-byte payload check is\n'
printf '  #   sudo profiles show -output stdout-xml — both empty on an unmanaged machine\n'

sec "Phase 3 — software distribution (needs the munki repo reachable)"
row 3.1 "the repository is a web server: the directory is closed, a catalog is served"
run "curl -so /dev/null -w '%{http_code}\n' $REPO_URL/"
for c in all testing; do
  run "curl -so /dev/null -w '%{http_code}\n' $REPO_URL/catalogs/$c"
done

sec "done — read-only; nothing above changed the machine"
