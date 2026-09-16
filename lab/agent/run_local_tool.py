#!/usr/bin/env python3
"""One task, one local model, ONE shell tool — the light tool-using path for a ledger row.

run.py is the no-tools bare-API path (classify a log, read a diff). Some rows need to *act* —
gather files, tar a bundle. This is those, kept as light as possible: the bare API against a
local model, one shell tool, a one-paragraph system line, no framework. It exists so a local
line for a tool-using row measures the model, not a 142K-token-per-turn agent CLI (row 3.3's
open follow-up).

    python3 run_local_tool.py --provider ollama --row T.1 --task task.md \
        --acceptance accept.md --workdir <a fresh dir with only the fixture>

The tool protocol is text, so it needs nothing from the model beyond following instructions:
the model writes `RUN: <one shell command>` to use the shell and stops; it gets the output back;
it writes `DONE: <final answer>` to finish. One command per turn, capped by --max-turns. The
command runs in --workdir with no network handed to it. Local host is AGENT_RUN_HOST (lab-host).
"""
from __future__ import annotations
import argparse, datetime as dt, os, pathlib, re, subprocess, sys, time

LOCAL_BASE = {"ollama": "http://localhost:11434/v1", "lmstudio": "http://localhost:1234/v1"}
DEFAULT_MODEL = {"ollama": "ornith-1.5:9b"}
SYSTEM = (
    "You are executing one responsibility from an endpoint-management runbook. Do exactly the "
    "task and nothing beyond it. You have ONE tool: a shell in the working directory. To run a "
    "command, write a line `RUN: ` followed by a single shell command and nothing after it, then "
    "stop; you will receive its output. When the task is complete, write `DONE: ` followed by "
    "your final answer. Never send, upload, or transmit anything anywhere."
)

def shell(cmd: str, workdir: str) -> str:
    p = subprocess.run(cmd, shell=True, cwd=workdir, capture_output=True, text=True,
                       timeout=60, env={"PATH": os.environ.get("PATH", "")})
    out = (p.stdout + p.stderr).rstrip()
    return out[:4000] + (f"\n… [{len(out)-4000} more chars]" if len(out) > 4000 else "")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="ollama", choices=["ollama", "lmstudio"])
    ap.add_argument("--model"); ap.add_argument("--row", required=True)
    ap.add_argument("--task", required=True, type=pathlib.Path)
    ap.add_argument("--acceptance", required=True, type=pathlib.Path)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--max-turns", type=int, default=14)
    ap.add_argument("--max-tokens", type=int, default=3000)
    ap.add_argument("--out-dir", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent.parent / "agent-runs")
    a = ap.parse_args()
    from openai import OpenAI
    model = a.model or DEFAULT_MODEL[a.provider]
    host = os.environ.get("AGENT_RUN_HOST", "lab-host")
    client = OpenAI(base_url=LOCAL_BASE[a.provider], api_key="local")
    task = a.task.read_text(); acceptance = a.acceptance.read_text()

    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
    transcript, cmds = [], 0
    started, t0 = dt.datetime.now(dt.timezone.utc), time.monotonic()
    stop = "max-turns"
    for _ in range(a.max_turns):
        r = client.chat.completions.create(model=model, messages=msgs, max_tokens=a.max_tokens)
        text = (r.choices[0].message.content or "").strip()
        transcript.append(f"**model:** {text}")
        msgs.append({"role": "assistant", "content": text})
        m = re.search(r"^RUN:\s*(.+)$", text, re.M)
        if "DONE:" in text or not m:
            stop = "done" if "DONE:" in text else "no-command"
            break
        cmd = m.group(1).strip().strip("`")
        out = shell(cmd, a.workdir); cmds += 1
        transcript.append(f"**shell** `{cmd}`:\n```\n{out}\n```")
        msgs.append({"role": "user", "content": f"Output of `{cmd}`:\n{out}"})
    wall = time.monotonic() - t0
    day = started.strftime("%Y-%m-%d")
    slug = re.sub(r"[^A-Za-z0-9.]+", "-", model).strip("-")
    path = a.out_dir / f"{day}-{a.provider}-{slug}-{a.row}.md"
    path.write_text(
        f"# Run — row {a.row} · {a.provider}:{model}@{host} · {day}\n\n"
        f"Path: local, one shell tool (run_local_tool.py)\n"
        f"Command: python3 lab/agent/run_local_tool.py {' '.join(sys.argv[1:])}   # cwd = a fresh dir with only the fixture\n"
        f"Model: {model}   Host: {host}\n"
        f"Started: {started.isoformat(timespec='seconds')}   Wall: {wall:.1f}s   Shell commands: {cmds}   Stop: {stop}\n\n"
        f"## Task\n{task.rstrip()}\n\n## Acceptance\n{acceptance.rstrip()}\n\n## Transcript\n"
        + "\n\n".join(transcript)
        + "\n\n## Result\nPENDING — read against the acceptance; PASS | FAIL | PARTIAL and one sentence.\nWhere the agent stopped: PENDING\n",
        encoding="utf-8")
    print(path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
