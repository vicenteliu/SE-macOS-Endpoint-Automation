#!/usr/bin/env python3
"""Turn an agent CLI's machine-readable transcript into the run record lab/agent-runs/ expects.

    python3 render_run.py --cli claude --events out.jsonl --row 3.3a --task task-a.md \
        --acceptance acceptance.md --command "claude -p ..." --out-dir ../agent-runs

`--cli claude` reads `claude -p --output-format stream-json --verbose` output.
`--cli codex`  reads `codex exec --json` output.
The Result section is left PENDING: pass/fail against the acceptance is a person's reading of
the transcript, and this script does not pretend otherwise.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys


def load(path: pathlib.Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def _clip(s: str, n: int = 4000) -> str:
    s = s.rstrip()
    return s if len(s) <= n else s[:n] + f"\n… [{len(s) - n} more characters]"


def render_claude(ev: list[dict]) -> tuple[str, dict]:
    lines, meta = [], {"model": None, "in": None, "out": None, "cost": None, "turns": None, "wall_ms": None, "stop": None}
    for e in ev:
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            meta["model"] = e.get("model")
        elif t == "assistant":
            msg = e.get("message", {})
            meta["model"] = msg.get("model") or meta["model"]
            for b in msg.get("content", []):
                if b.get("type") == "text" and b.get("text", "").strip():
                    lines.append(f"**assistant:** {_clip(b['text'])}\n")
                elif b.get("type") == "tool_use":
                    inp = b.get("input", {})
                    shown = inp.get("command") if isinstance(inp, dict) and "command" in inp else json.dumps(inp, ensure_ascii=False)
                    lines.append(f"**tool_use {b.get('name')}:** `{_clip(str(shown), 600)}`\n")
        elif t == "user":
            for b in e.get("message", {}).get("content", []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    lines.append("```\n" + _clip(str(c or "")) + "\n```\n")
        elif t == "result":
            u = e.get("usage", {})
            meta.update(cost=e.get("total_cost_usd"), turns=e.get("num_turns"), wall_ms=e.get("duration_ms"), stop=e.get("stop_reason") or e.get("subtype"),
                        **{"in": (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)) or None, "out": u.get("output_tokens")})
            if e.get("result"):
                lines.append(f"**final:** {_clip(e['result'])}\n")
    return "\n".join(lines), meta


def render_codex(ev: list[dict]) -> tuple[str, dict]:
    lines, meta = [], {"model": None, "in": None, "out": None, "cost": None, "turns": 0, "wall_ms": None, "stop": None}
    for e in ev:
        t = e.get("type", "")
        item = e.get("item") or {}
        it = item.get("type", "")
        if t == "thread.started":
            meta["model"] = e.get("model") or meta["model"]
        elif t == "item.completed":
            if it in ("agent_message", "assistant_message"):
                lines.append(f"**assistant:** {_clip(item.get('text') or item.get('content') or '')}\n")
            elif it == "command_execution":
                meta["turns"] += 1
                lines.append(f"**command:** `{_clip(item.get('command', ''), 600)}`  (exit {item.get('exit_code')})\n")
                lines.append("```\n" + _clip(item.get("aggregated_output") or "") + "\n```\n")
            elif it == "reasoning":
                pass  # summaries only; not evidence
            elif it not in ("todo_list",):
                lines.append(f"**{it}:** {_clip(json.dumps(item, ensure_ascii=False), 800)}\n")
        elif t == "turn.completed":
            u = e.get("usage", {})
            meta.update(**{"in": u.get("input_tokens"), "out": u.get("output_tokens")})
        elif t == "turn.failed" or t == "error":
            meta["stop"] = "error"
            lines.append(f"**error:** {_clip(json.dumps(e, ensure_ascii=False), 800)}\n")
    meta["stop"] = meta["stop"] or "end_turn"
    return "\n".join(lines), meta


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cli", required=True, choices=["claude", "codex"])
    ap.add_argument("--events", required=True, type=pathlib.Path)
    ap.add_argument("--row", required=True)
    ap.add_argument("--task", required=True, type=pathlib.Path)
    ap.add_argument("--acceptance", required=True, type=pathlib.Path)
    ap.add_argument("--command", required=True, help="the exact command line, keys as $VAR")
    ap.add_argument("--provider", required=True, help="anthropic | openai | ollama | lmstudio")
    ap.add_argument("--host", default="lab-host")
    ap.add_argument("--model", help="override the model id when the events do not carry it")
    ap.add_argument("--started", help="ISO timestamp; default: the events file's mtime")
    ap.add_argument("--wall", type=float, help="seconds, when the events do not carry it")
    ap.add_argument("--out-dir", required=True, type=pathlib.Path)
    a = ap.parse_args(argv)

    ev = load(a.events)
    body, meta = (render_claude if a.cli == "claude" else render_codex)(ev)
    model = a.model or meta["model"] or "unknown"
    started = dt.datetime.fromisoformat(a.started) if a.started else dt.datetime.fromtimestamp(a.events.stat().st_mtime, dt.timezone.utc)
    wall = a.wall if a.wall is not None else ((meta["wall_ms"] or 0) / 1000 or None)
    day = started.strftime("%Y-%m-%d")
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", model).strip("-")
    path = a.out_dir / f"{day}-{a.provider}-{slug}-{a.row}.md"
    record = f"""# Run — row {a.row} · {a.provider}:{model}@{a.host} · {day}

Path: cli ({a.cli})
Command: {a.command}
Model: {model}
Host: {a.host}
Started: {started.isoformat(timespec='seconds')}   Wall: {'—' if wall is None else f'{wall:.0f}s'}   Tokens: {meta['in']}/{meta['out']}   Cost: {'—' if meta['cost'] is None else f"${meta['cost']:.2f}"}   Turns: {meta['turns']}   Stop: {meta['stop']}

## Task
{a.task.read_text(encoding='utf-8').rstrip()}

## Acceptance
{a.acceptance.read_text(encoding='utf-8').rstrip()}

## Transcript
{body.rstrip() or '(no events)'}

## Result
PENDING — read the transcript against the acceptance; replace with PASS | FAIL | PARTIAL and one sentence.
Where the agent stopped: PENDING
"""
    a.out_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(record, encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
