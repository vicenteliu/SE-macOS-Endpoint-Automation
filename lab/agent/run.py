#!/usr/bin/env python3
"""One task, one model, one file in lab/agent-runs/ — the bare-API path for a ledger row.

Same task, same system line, same arguments against a hosted vendor or a local model, so the
rows in AGENT_BOUNDARY.md differ by model and by nothing else. No tools on purpose: this path
is for the narrow task (classify a log, propose an array, read a diff). A responsibility that
needs tools is run through an agent CLI instead — see lab/agent-runs/README.md.

    python3 run.py --provider anthropic --row 3.2 --task task.md --acceptance accept.md
    python3 run.py --provider openai    --model <exact id> --row 3.2 --task task.md --acceptance accept.md
    python3 run.py --provider ollama    --row 3.2 --task task.md --acceptance accept.md
    python3 run.py --provider lmstudio  --model <as LM Studio names it> --row 3.2 --task task.md --acceptance accept.md

Keys come from the environment only (ANTHROPIC_API_KEY, OPENAI_API_KEY) and are never written.
Local providers need no key; the record names the local host by AGENT_RUN_HOST (default
"lab-host"), never by the machine's own name. Requirements: requirements.txt next to this file.

Run state: the ollama path ran on 2026-09-15 (a one-word task, the record checked by hand); the
anthropic, openai and lmstudio paths are written to the same shape and have not yet been run.

Deliberately NOT enabled: the Anthropic API's server-side refusal fallback. A fallback would
answer the task on a different model than the one named, and the ledger exists to say which
model did what — a refusal is a result here, recorded as one, not routed around.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import pathlib
import re
import sys
import time

LOCAL_BASE = {"ollama": "http://localhost:11434/v1", "lmstudio": "http://localhost:1234/v1"}
DEFAULT_MODEL = {"anthropic": "claude-opus-5", "ollama": "ornith-1.5:9b"}
SYSTEM = (
    "You are executing one responsibility from an endpoint-management runbook. Do exactly the "
    "task and nothing beyond it. Produce what the acceptance criterion asks for. If you cannot, "
    "say precisely what stopped you instead of approximating."
)


def call_anthropic(model: str, task: str, max_tokens: int) -> dict:
    import anthropic  # official SDK; adaptive thinking is the model default and is left on

    r = anthropic.Anthropic().messages.create(
        model=model, max_tokens=max_tokens, system=SYSTEM,
        messages=[{"role": "user", "content": task}],
    )
    text = "".join(b.text for b in r.content if b.type == "text")
    return {"model": r.model, "text": text, "stop": r.stop_reason,
            "in": r.usage.input_tokens, "out": r.usage.output_tokens, "host": "api.anthropic.com"}


def call_openai_compatible(provider: str, model: str, task: str, max_tokens: int) -> dict:
    from openai import OpenAI

    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    if provider == "openai":
        host = "api.openai.com"
        r = OpenAI().chat.completions.create(model=model, messages=messages, max_completion_tokens=max_tokens)
    else:  # Ollama and LM Studio speak the same chat-completions shape on a local port
        host = os.environ.get("AGENT_RUN_HOST", "lab-host")
        client = OpenAI(base_url=LOCAL_BASE[provider], api_key="local")
        r = client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens)
    ch = r.choices[0]
    usage = r.usage
    return {"model": r.model, "text": ch.message.content or "", "stop": ch.finish_reason,
            "in": usage.prompt_tokens if usage else None, "out": usage.completion_tokens if usage else None, "host": host}


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "-", s).strip("-")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--provider", required=True, choices=["anthropic", "openai", "ollama", "lmstudio"])
    ap.add_argument("--model", help="exact model id; required for openai and lmstudio")
    ap.add_argument("--row", required=True, help="the AGENT_BOUNDARY.md row id, e.g. 3.2")
    ap.add_argument("--task", required=True, type=pathlib.Path, help="task.md, verbatim into the record")
    ap.add_argument("--acceptance", required=True, type=pathlib.Path, help="the row's 'How you know it worked', verbatim")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent.parent / "agent-runs")
    a = ap.parse_args(argv)

    model = a.model or DEFAULT_MODEL.get(a.provider)
    if not model:
        ap.error(f"--model is required for {a.provider}")
    task, acceptance = a.task.read_text(encoding="utf-8"), a.acceptance.read_text(encoding="utf-8")

    started = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    res = call_anthropic(model, task, a.max_tokens) if a.provider == "anthropic" else call_openai_compatible(a.provider, model, task, a.max_tokens)
    wall = time.monotonic() - t0
    finished = dt.datetime.now(dt.timezone.utc)

    day = started.strftime("%Y-%m-%d")
    path = a.out_dir / f"{day}-{a.provider}-{slug(res['model'])}-{a.row}.md"
    argv_shown = " ".join(sys.argv[1:])
    record = f"""# Run — row {a.row} · {a.provider}:{res['model']}@{res['host']} · {day}

Path: api
Command: python3 lab/agent/run.py {argv_shown}
Model: {res['model']}  (requested: {model})
Host: {res['host']}
Started / finished: {started.isoformat(timespec='seconds')} / {finished.isoformat(timespec='seconds')}   Wall: {wall:.1f}s   Tokens: {res['in']}/{res['out']}   Stop: {res['stop']}

## Task
{task.rstrip()}

## Acceptance
{acceptance.rstrip()}

## Transcript
{res['text'].rstrip()}

## Result
PENDING — check the transcript against the acceptance and replace this line with PASS | FAIL | PARTIAL and one sentence.
Where the agent stopped: PENDING
"""
    a.out_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(record, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
