# Specced-Not-Run is a third marker, not a missing one

This repository inherits a two-marker honesty system — 🔨 operated for real, 🧭 mapped and
doc-checked but not run — and adds a third: ⛔ **Specced-Not-Run**.

The obvious reading is that ⛔ is just 🧭 with extra words, and that adding a marker to a
system whose whole value is that it is small makes it worse. That reading is why this is
written down.

## The difference

🧭 is *doc-checked with no plan to execute*. ⛔ carries the complete environment
specification, the step-by-step verification, the acceptance criteria, and **an explicit
stated reason for not executing**. One is an absence. The other is a decision.

Network access (phase 4) is the first and currently only ⛔. Standing up 802.1X honestly
requires a certificate authority, an authentication server and a handshake against real
network hardware. On a single machine that is also the working machine, the failure mode is
losing the network — not losing an afternoon. That is a cost decision with a stated price,
and collapsing it into 🧭 would hide the one thing worth publishing about it.

## Why it earns its own symbol

Because the two are read differently by the only audience that matters. *"I have not done
that"* and *"here is the environment I specified to do it, what each tier can and cannot
verify, and why the tier I have stops short of the handshake"* are different answers to the
same question, and the second is only available if the distinction was made while writing.

A reader who wants to build this can act on a ⛔ section. They cannot act on a 🧭 one.

## Rejected

- **Folding it into 🧭.** Loses the specification, which is the publishable part.
- **Marking it 🔨 because the design was done.** Designing is not running. That is precisely
  the overclaim the marker system exists to prevent.
- **Leaving phase 4 out entirely.** A chain with a hole where the hard hop goes is not an
  honest chain, and the hole is the most instructive part of it.
