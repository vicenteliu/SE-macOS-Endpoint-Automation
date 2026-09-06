# Phase 5 — Identity

> ⚠️ **An optional extension, and labelled one on purpose.** The chain this repository documents
> reaches a usable machine without it. It is here because identity is where a real estate ends up,
> not because the chain requires it — and putting it level with the required phases would be
> prioritising by interest rather than by need.

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **The attachment question** | 🧭 | Local account or directory account at first login, and what each costs later |
| 2 | 🥇 **The trust boundary** | 🔨 | Which certificate authority a given endpoint can be told to trust — and why that is the same question as [phase 4](../4-network-access/) |
| 3 | **Attachment options** | 🧭 | What the products do, without claiming to have operated them |

🔑 **The marker split here is the honest one and it is not the obvious one.** Identity as a
discipline is hands-on: a directory built and run, schema extended with custom attributes,
master–replica replication configured, LDAPS terminated against two different certificate
authorities for a stated reason, and a tool written to push a single user downstream ahead of the
scheduled cycle. **What is a ramp is the macOS-side attachment specifically** — the endpoint half,
not the directory half.

## Prerequisites

A machine that is configured and on the network ([phases 2](../2-configuration/) and
[4](../4-network-access/)). ⛔ Identity attachment is the last hop for a reason: it is the one that
fails hardest when the ones before it are shaky.

## Hop 1 — the attachment question 🧭

At first login there is one decision with a long tail: **is the account on this machine a local
account, or an account the directory owns?**

- **Local** — the machine works when nothing else does. Offboarding, password policy and audit are
  yours to build, and they will be built badly because they are nobody's project.
- **Directory-backed** — one place to disable someone, one password policy, one audit trail. And a
  dependency on the identity provider being reachable at the exact moment a person is trying to
  start work.

⛔ **Mapped, not run** for the macOS-specific mechanisms. This document does not describe how to
operate them; the trade-off above is what it can speak to.

## Hop 2 — 🥇 the trust boundary

**This is the hop with something behind it, and it is the same problem [phase 4](../4-network-access/)
solves from the other side.**

A directory service terminating LDAPS was fronted by **two different certificate authorities**, and
the reason is the whole point:

> Internal services trusted the internal authority. But the endpoint that **unmanaged personal
> devices** reached needed a **publicly-trusted** certificate — **because you cannot push a private
> root onto a device you do not manage.**

🔑 **Phase 4 is that sentence with the sign flipped.** Certificate-based network access works
*precisely because* the device is managed: a private root and an enrolment identity can be placed
on it, so a private authority is sufficient and a public one is unnecessary.

**Same boundary, opposite sides.** Which certificate authority an endpoint can be told to trust is
a property of whether you manage it — and that single question decides the certificate strategy
for the network, the directory, and every internal service behind them. An estate that answers it
once, deliberately, ends up with two authorities and a clear rule about which endpoints reach
which service. An estate that answers it per-project ends up with a public certificate on
everything and no idea why.

## Hop 3 — attachment options 🧭

Directory-backed login, single sign-on at the operating-system layer, and the products that connect
them. The selection criteria are stable: does it hold when the provider is unreachable, does it
survive a password change made somewhere else, and does it leave the machine usable if you remove
it.

⛔ **This document does not speak from operating a named product here** and lists selection
criteria rather than vendors it has read about.

## How this phase fails

🥇 **The deadlock, and it is the same shape as [phase 4](../4-network-access/)'s expired
certificate**: the account is directory-backed, the identity provider is unreachable, and **nobody
can log in to the machine that would be used to fix it.** A phase-4 failure and a phase-5 failure
present identically to the person holding the laptop — no access, no obvious cause — and the first
diagnosis is usually the wrong one.

Two more:
- **A password changed somewhere else.** The directory knows; the machine does not, until it can
  reach the directory. The gap between those two facts is where the support calls live.
- **Offboarding that stops at the directory.** Disabling an account is not the same as a machine
  forgetting a cached credential, and the difference is measured in days on a device nobody has
  collected yet.

## Verification

| | Check | Expect |
|---|---|---|
| 1 | Log in on a machine with the identity provider unreachable | A stated, intended outcome — **not a discovery** |
| 2 | Enumerate which endpoints are reached by unmanaged devices | Each one served by a publicly-trusted certificate. **An internal authority on any of them is the finding** |
| 2 | Enumerate which are reached only by managed devices | An internal authority is correct and sufficient here. A public certificate is money spent for nothing |
| 3 | Change a password in the directory, then log in on the machine | The behaviour is the one you documented, at the interval you documented |
| 3 | Disable an account, then attempt login on a machine that is offline | The outcome is known in advance. If nobody knows, that is the answer |

## Acceptance

> **Both certificate authorities are deliberate.** Every endpoint an unmanaged device reaches is
> publicly trusted, every endpoint only managed devices reach is internally trusted, and someone
> can say which is which without looking it up.

⛔ Not "single sign-on works." That is a demonstration. The acceptance criterion is that the trust
boundary was *decided* rather than accumulated — because the alternative is invisible until an
audit or an outage makes it visible.

## Escape Hatch

🔴 **A local account that exists, and whose password somebody knows.**

Every directory-backed estate needs one, and the reason it gets skipped is that it looks like a
hole in exactly the control you just built. It is not a hole; it is the thing that makes the
control survivable. The identity provider will be unreachable one day, and on that day the
question is whether anyone can get into the machine at all.

- **Have it, document that it exists, and rotate it.** An emergency account nobody can find is the
  same as not having one.
- ⛔ **Do not make it the same credential everywhere.** The reason this hatch is skipped is a real
  risk, and the answer to that risk is scope and rotation, not absence.
- **Know what a disabled account does to a machine that is offline**, before you need to know.
