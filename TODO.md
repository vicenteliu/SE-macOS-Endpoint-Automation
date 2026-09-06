# What gets written next, and why in this order

Architecture first, content progressively. This file is the order and the reasoning — a
heading with no body in this repository means *not yet done*, not *forgotten*.

## The rule this order follows

**Depth first, not breadth.** One phase filled completely is worth more than one section
filled everywhere, because the thing a reader cannot currently judge is *what a finished
section looks like here*. Markers in a table are a promise; a worked section is the evidence.

---

## 1. ✅ Phase 3 — software distribution 🔨 — **written 2026-09-05**

Why it was first: it is the only phase a reader can execute. "Reference implementation" means
someone else can run it, and phase 3 is the one with a repository model, real commands, and a
verifiable end state. Phases 0, 5 and 6 have no worked material behind them yet; phase 4 is a
specification rather than something runnable.

- [x] Repository model — the server is a web server, the client decides
- [x] 🥇 Version comparison **and** blocking derivation from the same metadata array — including
      the observed behaviour where a running application is refused *after* the payload is
      already downloaded
- [x] Packaging automation — processor chains, overrides, and trust pinning as a supply-chain
      control
- [x] Package internals 🧭 — payload vs payload-free, install scripts, signing, notarisation
- [x] Verification block: the exact commands and the exact expected log lines
- [x] Escape Hatch

⛔ **The boundary ships with it, every time**: one machine, one afternoon, two applications, no
fleet. The claim is *the pipeline was stood up end to end and it is known where it bites* — not
operational experience at scale.

## 2. ✅ Phase 4 — network access ⛔ Specced-Not-Run — **written 2026-09-05**

**Why second, and why it is not optional:** this repository added a third marker and gave it its
own ADR. Right now **⛔ appears in a table cell and nowhere else**. An ADR that argues for a
distinction the repository never demonstrates is the weakest position available — and this is
also the unusual half. Every macOS repository has a software-distribution section; almost none
publishes a complete specification for the thing its author deliberately did not run, with the
exact hop each lab tier cannot prove.

- [x] The three roles and the handshake; EAP-TLS as mutual certificate authentication
- [x] Credential delivery — how a machine that has never been touched ends up holding a private
      key, and why the identity payload must be bound to the network payload
- [x] 🥇 The deadlock: certificate expires → no network → cannot reach the management server that
      would renew it. This is the actual hard problem, not the handshake
- [x] Tier specification: what minimum / mid / full each verify, and **the exact hop each stops at**
- [x] Escape Hatch — what happens to a machine that cannot authenticate is a business decision,
      not a networking one

## 3. ✅ Phase 2 — the currency pass ⏰ — **written 2026-09-05, while it was still imminent**

Why it was time-sensitive: the accurate 2026 statement is that configuration profiles are
**not deprecated — they are being subsumed**. Declarative management is the delivery and
enforcement model, and from OS 27.0 a legacy profile can be carried as a declarative asset. What
genuinely stops functioning at 27.0 is *legacy software update management* — the commands,
queries, cadence settings and deferrals.

⏰ **This is worth most while it is still imminent.** Once 27.0 ships it becomes ordinary
history, and a page that says it early reads differently from one that says it late.

- [x] Fold the above into the configuration phase and the chain
- [x] Payload structure, identifiers, signing, removability, device vs user scope
- [x] The identifier-collision failure and the locked-profile trade-off
- [x] Escape Hatch

## 4. ✅ EXPLAIN.md — **written 2026-09-05**

Originally blocked on 1: The translation needs a completed phase to translate, and phase 3 is the right
first subject because it is the one with a real run behind it. Translating a specification would
demonstrate the method on the easiest possible case.

- [x] The one-sentence outcome
- [x] Per-phase table: who notices · what they cannot do · time to recover
- [x] What this does not solve
- [x] Verify it with the only question that matters: *what would you decide differently after
      reading this?* — "that was clear" is a failure, not a pass

📌 **Still owed on this one**: the verify question has not been put to an actual reader. Until it
has, the page is drafted rather than tested — and it is the one page here whose acceptance
criterion cannot be met alone.

## 5. ✅ Phase 6 — operations — **written 2026-09-05**

🔴 **Two corrections to what this file used to say**, both found by being asked why a phase was
missing rather than by reviewing it.

**It grouped phases 0, 5 and 6 as** *"none of these has worked material behind it."* That was true
of one of them.

🔴 **And phase 1 was never in this file at all.** Not a decision — an omission. Its material was
ready the same day the first phases were written. Written 2026-09-05.

- **Phase 0 is gone.** Not unwritten — *redundant*. Tier selection and product selection are
  already `docs/02` and `docs/01`, and administrator prerequisites belong per-phase because they
  differ per phase. Removed rather than left as an empty directory implying content was coming.
- **Phase 6 is more written than it was described as.** Its third hop *is* `EXPLAIN.md`, already
  done. Its first hop — queue ownership, severity as lived practice rather than vocabulary, what
  gets escalated and what gets kept — has real material behind it and is publishable as method.

- [x] Hop 1 — queue and escalation 🔨: severity as a lived scheme, tiering, and what a support
      organisation owes a population more technical than itself
- [x] Hop 2 — support tooling 🧭: a boundary line, stated as one
- [x] Hop 3 — explaining it → `EXPLAIN.md`
- [x] Escape Hatch

## 6. Phase 5 — identity, optional — **the only phase left**

⛔ **The one that genuinely has nothing behind it.** A ramp, and the chain it belongs to names no
identity provider as a requirement. Writing it from documentation alone would make this a summary
of other people's pages — the one thing the marker system exists to prevent. It stays a skeleton
until that changes.

## Also later

Per-product detail in the selection document; build instructions per lab tier; putting
`EXPLAIN.md`'s verify question to an actual reader.
