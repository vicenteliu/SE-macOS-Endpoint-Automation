# Run — row probe · ollama:ornith-1.5:9b@lab-host · 2026-09-15

Path: cli (codex)
Command: codex exec --oss --local-provider ollama -m ornith-1.5:9b --json -s read-only --skip-git-repo-check -o last.md "<task>"   (the operator's own CODEX_HOME; a second probe with a clean CODEX_HOME sent the same 141K-token prompt and was stopped)
Model: ornith-1.5:9b
Host: lab-host
Started: 2026-09-15T07:44:12+00:00   Wall: 1266s   Tokens: None/None   Cost: —   Turns: 1   Stop: end_turn

## Task
Run the shell command 'ls /Users/Shared/munki_repo' and reply with the directory names it printed.

## Acceptance
The reply lists exactly the five directories the command prints: catalogs, icons, manifests, pkgs, pkgsinfo. This is a harness probe, not a ledger row: it measures whether the CLI + local model can complete one tool call at all, and how long that takes.

## Transcript
**error:** {"id": "item_0", "type": "error", "message": "Model metadata for `ornith-1.5:9b` not found. Defaulting to fallback metadata; this can degrade performance and cause issues."}

**error:** {"id": "item_1", "type": "error", "message": "Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest."}

**assistant:** I'll run that command and report the directory names.

**command:** `/bin/zsh -lc 'ls /Users/Shared/munki_repo'`  (exit 0)

```
catalogs
icons
manifests
pkgs
pkgsinfo
```

## Result
PASS on the answer, FAIL on cadence — the five names are right; it took 21 minutes over two turns, because the CLI's local-provider path sent a 142,724-token prompt and then a 147,467-token one (Ollama server log: `task.n_tokens`), processed at ~245 tokens/s on this GPU with no cache reuse between turns. The model is not the bottleneck; the harness is.
Where the agent stopped: nothing to reverse. One `ls`, one correct reply.
