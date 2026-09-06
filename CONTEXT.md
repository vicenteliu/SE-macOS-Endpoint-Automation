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
