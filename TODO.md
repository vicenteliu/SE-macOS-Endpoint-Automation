# What gets written next, and why in this order

Architecture first, content progressively. This file is the order and the reasoning — a
heading with no body in this repository means *not yet done*, not *forgotten*.

## The rule this order follows

**Depth first, not breadth.** One phase filled completely is worth more than one section
filled everywhere, because the thing a reader cannot currently judge is *what a finished
section looks like here*. Markers in a table are a promise; a worked section is the evidence.

---

## 1. ✅ Phase 3 — software distribution 🔨 — **written 2026-09-05**

➡️ **Next up is section 2.** — Why it was first: it is the only phase a reader can execute. "Reference implementation" means
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

## 2. Phase 4 — network access ⛔ Specced-Not-Run

**Why second, and why it is not optional:** this repository added a third marker and gave it its
own ADR. Right now **⛔ appears in a table cell and nowhere else**. An ADR that argues for a
distinction the repository never demonstrates is the weakest position available — and this is
also the unusual half. Every macOS repository has a software-distribution section; almost none
publishes a complete specification for the thing its author deliberately did not run, with the
exact hop each lab tier cannot prove.

- [ ] The three roles and the handshake; EAP-TLS as mutual certificate authentication
- [ ] Credential delivery — how a machine that has never been touched ends up holding a private
      key, and why the identity payload must be bound to the network payload
- [ ] 🥇 The deadlock: certificate expires → no network → cannot reach the management server that
      would renew it. This is the actual hard problem, not the handshake
- [ ] Tier specification: what minimum / mid / full each verify, and **the exact hop each stops at**
- [ ] Escape Hatch — what happens to a machine that cannot authenticate is a business decision,
      not a networking one

## 3. Phase 2 — the currency pass ⏰

**Why it is time-sensitive:** the accurate 2026 statement is that configuration profiles are
**not deprecated — they are being subsumed**. Declarative management is the delivery and
enforcement model, and from OS 27.0 a legacy profile can be carried as a declarative asset. What
genuinely stops functioning at 27.0 is *legacy software update management* — the commands,
queries, cadence settings and deferrals.

⏰ **This is worth most while it is still imminent.** Once 27.0 ships it becomes ordinary
history, and a page that says it early reads differently from one that says it late.

- [ ] Fold the above into the configuration phase and the chain
- [ ] Payload structure, identifiers, signing, removability, device vs user scope
- [ ] The identifier-collision failure and the locked-profile trade-off
- [ ] Escape Hatch

## 4. EXPLAIN.md

**Blocked on 1.** The translation needs a completed phase to translate, and phase 3 is the right
first subject because it is the one with a real run behind it. Translating a specification would
demonstrate the method on the easiest possible case.

- [ ] The one-sentence outcome
- [ ] Per-phase table: who notices · what they cannot do · time to recover
- [ ] What this does not solve
- [ ] Verify it with the only question that matters: *what would you decide differently after
      reading this?* — "that was clear" is a failure, not a pass

## Later

Phases 0, 5 and 6; per-product detail in the selection document; build instructions per lab tier.
None of these has worked material behind it yet, and writing them from documentation alone would
make this a summary of other people's pages — which is the one thing the marker system exists to
prevent.
