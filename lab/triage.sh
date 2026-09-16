#!/bin/bash
# lab/triage.sh — a demonstrative troubleshooting-automation flow.
#
# Four stages, and the fourth is a wall: collect → classify → propose → STOP at the human gate.
# Everything before the gate is read-only or a recommendation; nothing is remediated. It wires the
# pieces this repository already has — the read-only capture (verify.sh / ledger T.1), the model
# classify (run.py / ledger T.2), and docs/05's per-symptom remediation with its 🤖/🔴 marks.
#
# Demonstrated on the synthetic fixture (the minimum tier has no managed fleet); the identical flow
# runs against a real host by collecting from it instead of reading the fixture. It is a THINKING
# aid and a demo, not a product: the point it makes is where the automation stops.
#
#   bash lab/triage.sh                 # uses the T.1/T.2 fixture; classifies with the local model
#   FIXTURE=<dir> bash lab/triage.sh   # point it at another captured-diagnostics directory
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FIXTURE="${FIXTURE:-$HERE/agent/docs05-rowsT.1-T.2/fixture}"
MODEL="${TRIAGE_MODEL:-ornith-1.5:9b}"
step(){ printf '\n\033[1m===== %s =====\033[0m\n' "$*" 2>/dev/null || printf '\n===== %s =====\n' "$*"; }

step "STAGE 1 · COLLECT  (🤖 read-only — a script may do this unattended)"
echo "  captured diagnostics from the host, read-only, in: $FIXTURE"
ls "$FIXTURE" | sed 's/^/    /'
BUNDLE="$(for f in "$FIXTURE"/*; do echo "--- $(basename "$f") ---"; cat "$f"; echo; done)"
echo "  bundle assembled ($(printf '%s' "$BUNDLE" | wc -l | tr -d ' ') lines). NOT sent anywhere — that is a person's act."

step "STAGE 2 · CLASSIFY  (🤖 a model names the probable cause with its evidence line)"
CAUSE="$(BUNDLE="$BUNDLE" MODEL="$MODEL" python3 - <<'PY'
import os
from openai import OpenAI
c=OpenAI(base_url="http://localhost:11434/v1", api_key="local")
sys=("You are triaging one macOS host from its read-only diagnostics. Name the single most likely "
     "cause of a setting not being in effect, in ONE sentence, and cite the file(s) that support it. "
     "Do not propose or perform any remediation.")
r=c.chat.completions.create(model=os.environ["MODEL"],
    messages=[{"role":"system","content":sys},{"role":"user","content":os.environ["BUNDLE"]}],
    max_tokens=1200)
print((r.choices[0].message.content or "").strip())
PY
)"
echo "$CAUSE" | sed 's/^/  /'

step "STAGE 3 · PROPOSE  (🤖 name the remediation from docs/05 — 🔴 mark what a person must gate)"
# A real pipeline keys the lookup off the classified cause; for the demo the one symptom class is
# 'a scoped profile the console believes installed is absent on the device' (docs/05 symptom B).
case "$CAUSE" in
  *[Pp]rofile*|*restrictions*|*scoped*)
    echo "  symptom class: docs/05 · B — a profile applied in the console but not in effect"
    echo "    🤖 automatable: re-push the profile (reversible — the payload replaces itself)"
    echo "    🤖 automatable: re-check the device with 'profiles list' afterwards (read-only)"
    echo "    🔴 GATE (a person): if it is a non-removable profile, do NOT unset it — that is a future wipe"
    echo "    🔴 GATE (a person): if the host has not checked in, decide re-enrolment — which on a supervised Mac is a wipe";;
  *) echo "  (no mapping for this cause in the demo's table — a person reads docs/05 and decides)";;
esac

step "STAGE 4 · THE GATE  (🔴 nothing above changed the host; a person decides from here)"
echo "  Proposed, not run. A person confirms the 🔴 items and runs them."
echo "  Severity and the trigger to remediate stay with a person by design (ledger T.3, ⛔)."
echo "  Rule: the line is the cost of being wrong on THIS machine, not the difficulty of the command."
