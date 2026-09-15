# Context

The vocabulary this repository uses, and what each word is chosen *against*. Terms are
defined by what they **are**, not by what they do.

## Language

**Playbook**:
What this repository is: the **Chain**, one **Runbook** per phase, and the decisions between
them — written first for a reader with five minutes and second for whoever runs a fleet from
it. Not a reference architecture, which promises diagrams where this has commands.
_Avoid_: "method repository," "portfolio," "reference architecture," "framework"

**Chain**:
The ordered set of hops between a sealed box and a machine someone can work on. Named as a
chain because the interesting failures are at the joints, not inside the links.
_Avoid_: "workflow," "pipeline," "onboarding flow"

**Hop**:
One transition in the **Chain**, owned end to end by one mechanism. A hop is the unit that
gets verified; a phase is the boundary of **Acceptance** — what proves a phase is usually one
outcome across several hops — and is published as one **Runbook**.
_Avoid_: "step," "stage," "task"

**Runbook**:
One phase, as published: prerequisites, its **Hops**, how the phase fails, a verification row
per hop, one **Acceptance**, one **Escape Hatch**. A command appears wherever a **Lab Tier** can
produce it; a script appears only where one was run.
_Avoid_: "guide," "procedure," "SOP," "checklist"

**Lab Tier**:
One of three declared environment levels — minimum, mid, full — each stating exactly which
**Hop** it can verify *and which it cannot*. The boundary is the payload: a tier whose
limits are unstated is a runbook, and a tier that names them is an honest answer about
scope.
_Avoid_: "environment," "setup," "tier" (unqualified)

**Specced-Not-Run** (⛔):
Work carrying a complete environment specification, step-by-step verification and
acceptance criteria, deliberately **not executed**, with the reason stated. Distinct from
🧭, which is doc-checked with no plan to execute.
_Avoid_: "planned," "TODO," "future work," "not done"

**Acceptance**:
The condition under which a **Hop** is finished — a command and its expected output, never
a feeling that it worked. A hop with no stated acceptance is not designed, it is described.
_Avoid_: "definition of done," "success criteria," "testing"

**Escape Hatch**:
The stated path for a user the design would otherwise block. Every phase has one, because a
population that out-technicals its support organisation routes around a control it cannot
negotiate with — and an undocumented workaround is worse than a documented exception.
_Avoid_: "exception," "override," "bypass"

**Responsibility Item**:
One duty from the chain, concrete enough that the line between what a person decides and what
a model executes can be drawn through it and argued — a row in the **Agent Boundary Ledger**.
Taken from a **Runbook** hop or a docs/03 row, never invented for the ledger.
_Avoid_: "task," "duty," "use case," "job"

**Agent Boundary Ledger** (`AGENT_BOUNDARY.md`):
One row per **Responsibility Item**, four lines each — *Human decides / Agent executes / How /
How you know it worked* — and a **model line**: the exact model identifier, where it ran, the
date. A row is 🔨 only when an **Agent Run** stands behind it; a model that did not run the
task has no line; when a model generation changes the old line stays and a new one is added,
because the ledger's payload is the boundary *moving*, which a snapshot cannot show. A model
line older than 90 days, or from a superseded generation, is ⏳ until re-run (ADR-0002).
_Avoid_: "AI policy," "automation matrix," "capability map," "what AI can do"

**Agent Run**:
One file in `lab/agent-runs/` — the command, the model as the endpoint reported it, the task
and acceptance verbatim, the complete transcript, and the pass/fail against the acceptance.
Made through an agent CLI when the responsibility needs tools, through the bare API when it
does not, and the file says which. It is the credential behind a ledger row, screened for
secrets before it is committed.
_Avoid_: "experiment," "eval," "benchmark," "demo"

**Verification row** (rule, ADR-0002):
A command or an API call and what it must return. A row that names only a check is a debt,
listed in docs/04 with the command that could clear it. A row that only a graphical console
can satisfy is allowed, marked ⚠️ GUI-only, and carries the reason. Sections written after
2026-09-15 open with *Before you start · Permissions · Minimum test · Verify · Rollback*.
_Avoid_: "manual check," "eyeball," "confirm in the console"
