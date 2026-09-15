# A verification row is a command or an API call, and the agent boundary is a ledger with a date on every model

Two things this repository did not say, and now does.

The first: its verification tables mixed rows that name a command with rows that name a check
— *inspect the enrolled record*, *compare what was uploaded with what landed*. A reader running
the phase on arrival cannot tell whether the second kind means a command they have not been
given or a console they are expected to open. The distinction is the whole difference between
a runbook and a description.

The second: the question every reader now brings — *which of this can I hand to a model?* — was
answered nowhere, and an answer given in prose would be wrong within a model generation.

## Decision

**1. A verification row is a command or an API call, plus what it must return.**
Where the check has no command yet, the row says which lab tier could produce one. A row that
can only be done in a graphical console is allowed, but it is marked **⚠️ GUI-only** and carries
the reason — usually *no API exposes this* — so that the day an API appears, the row is a
known debt rather than a habit. The audit of the existing rows is
[docs/04](../04-verification-audit.md); nothing was rewritten to pass it, the audit lists.

**2. Every runbook section written from now on opens with the same five headings**, in this
order: **Before you start** (host, VM, OS version) · **Permissions** (which role, which token,
which scope) · **Minimum test** (the smallest fixture that proves the hop) · **Verify** (the
command or call, and the expected output) · **Rollback**. Sections already written are not
back-filled; they get the block when they are next touched. A back-fill would be a rewrite of
material nobody re-ran.

**3. The agent boundary is a ledger, [`AGENT_BOUNDARY.md`](../../AGENT_BOUNDARY.md)**, one row
per **Responsibility Item**, four lines per row — *Human decides / Agent executes / How / How you
know it worked* — and a **model line**: the exact model identifier, where it ran, and the date.
A model that did not run the task has no line. A run leaves a file in
[`lab/agent-runs/`](../../lab/agent-runs/), and that file is the only thing that turns a 🧭 row
into a 🔨 one. When a model generation changes, the old line stays and a new one is added:
the ledger is meant to show the boundary moving, which a snapshot cannot. A line older than 90
days, or from a superseded generation, is ⏳ and is re-run before it is cited.

**4. A run is made in one of two ways, and the record says which.** An agent CLI (`claude -p`,
`codex exec`; a local model through `codex exec --oss --local-provider ollama|lmstudio`) is the
main path, because a responsibility is executed with tools, not answered. A bare API call
(`lab/agent/run.py`) is for the narrow task — classify a log, propose an array — where tools
would be theatre. Each responsibility is tried on **at least three** models: the current
default from two hosted vendors and one local model, so that the hosted/local gap is visible on
the same task, in the same table.

**5. Transcripts are public, so they are screened.** Keys live in the environment and never in a
file; `lab/check_secrets.sh` runs over `lab/agent-runs/` before anything is committed and a hit
refuses the commit. The same de-identification pass as every other page applies — no employer,
no fleet, no hostname that is not the lab's.

## Why a ledger and not a section per phase

Because the interesting fact is not *where the line is* but *that it moves*, and the only way
to show movement honestly is the same row with two dates on it. A prose section per phase
would be rewritten each time and lose the history; a row per model keeps it. This is also why
rows are never invented ahead of a run: a ledger of predictions is a blog post.

## What this does not change

The markers (🔨 🧭 ⛔, ADR-0001). The rule that a script appears only where one was run. The
private/public split. A row in the ledger being 🧭 says nothing about whether the *human* ran
the hop — that is the runbook's marker, and phase 3's hops are 🔨 there while every ledger row
under them starts at 🧭, because nobody has handed them to a model yet.
