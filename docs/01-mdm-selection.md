# Choosing the management layer

## Disclosure, first

The author maintains [`muster`](https://github.com/vicenteliu/muster), an open-source fleet
agent. **It is not a candidate below.**

Saying so is cheaper than leaving it to be discovered. A vendor-neutral comparison written
by someone shipping a product in the same category stops reading as a framework and starts
reading as a pitch, and a reader cannot un-notice that once they have noticed it. Keeping
`muster` out protects the comparison's neutrality and lets `muster` remain what it is — a
build-to-learn project, not a candidate in its author's own selection framework.

It also does not implement the Apple MDM protocol, so it is not an alternative to anything
here on the merits either.

## The candidates, and what may honestly be said about each

| | Marker | What that means here |
|---|---|---|
| **Jamf Pro** | 🔨 bounded | Operated: console work, policy and profile scoping, and the API driven for both inventory reads and policy writes. Bounded to a regional testing-and-maintenance remit within a larger estate — not tenant ownership |
| **Workspace ONE / UEM** | 🔨 | Operated: a BYOD programme end to end, and application distribution targeted by user, group, region and country |
| **Microsoft Intune** | 🧭 | **Never run.** The API surface and the management model are mapped; nothing here says how to operate it |
| **Kandji** | 🧭 | **Never run.** Present because it changes the answer for some fleet shapes, not because of experience with it |

⛔ **Consequence, stated rather than implied**: for the two marked 🧭 this document says
what they solve and what they cost. It never says how to operate them, and no sentence here
should be readable as operating experience.

## The axis that actually decides it

Not the feature matrix. Three questions, in this order:

1. **What is the licensing unit — the device or the person?** This inverts the cost answer
   depending on how many devices each human carries, and it is the single largest driver at
   any real fleet size. Two organisations of identical headcount land on different products
   for this reason alone.
2. **What else is already in the building?** A management layer that shares an identity
   provider and a compliance surface with what is already deployed is cheaper than its
   licence line suggests. One that does not is more expensive than its licence line
   suggests.
3. **How many administrators, and what is their day actually made of?** Fleet size does not
   set staffing; the ratio between them varies by roughly an order of magnitude across real
   organisations, and the variable is how much of the estate is exception rather than
   standard.

## Per-product detail — each against the three questions

Read down the axes above, not across a feature grid. For the two 🔨 products the detail includes
what operating them was; for the two 🧭 it stops at what they solve and what they cost, because
nothing here operated them.

### Jamf Pro — 🔨 bounded

- **Licensing unit: the device.** Per-device pricing, so its cost answer is set by the device
  count, not the headcount — the opposite of Intune, and the reason two identical-headcount
  estates diverge (axis 1).
- **What it assumes in the building:** an Apple-majority estate. Jamf is Apple-only and deep on
  it — same-day support for new OS releases, the fullest MDM surface Apple exposes. It shares
  nothing with a Windows-management or M365 compliance surface, so on a mixed estate its licence
  line understates its true cost (axis 2).
- **What its day is made of:** flexibility bought with build effort — Smart Groups, extension
  attributes, policy and profile scoping, and an API that both reads inventory and writes policy.
  The admin ratio is set by how much of the estate is exception (axis 3); Jamf rewards a team that
  will build, and punishes one that wanted defaults. *Operated here* to that description, bounded
  to a regional testing-and-maintenance remit within a larger estate — not tenant ownership.

### Workspace ONE / UEM — 🔨

- **Licensing unit: device or named user** — it sells both, so axis 1 is a choice rather than a
  given, which matters most where each person carries several devices.
- **What it assumes in the building:** a **multi-platform** estate. Its reason to exist over an
  Apple-only tool is iOS, Android, macOS and Windows under one console and one policy model; on a
  single-platform fleet that breadth is paid for and unused.
- **What its day is made of:** targeting. *Operated here* end to end for a BYOD programme and for
  application distribution scoped by user, group, region and country — the assignment model is the
  product, and getting the scoping right is most of the work.

### Microsoft Intune — 🧭 (never run)

- **Licensing unit: the person.** Bundled into M365 E3/E5 and EMS, so for an organisation already
  on those it can arrive at *no marginal licence line at all* — the single largest reason it wins
  regardless of Apple-management depth (axis 1 and 2 pulling together).
- **What it solves:** one management and compliance surface across Windows, Apple and Android,
  sharing Entra identity and Microsoft's compliance signals with everything else already deployed —
  precisely the axis-2 saving.
- **What it costs:** Apple-management depth shallower than Jamf's, later support for new Apple OS
  releases, and a dependency chain (Apple Business Manager, APNs, the connector) that is a fleet's
  problem the day it lapses. *How to operate it is not stated here — it has not been run.*

### Kandji — 🧭 (never run)

- **Licensing unit: the device**, Apple-only.
- **What it solves:** time-to-value. Pre-built Blueprints, guardrails and compliance templates
  answer for a lean team what Jamf answers with build effort, which changes the axis-3 answer for a
  small-to-mid Apple-only fleet whose admin day cannot be spent building.
- **What it costs:** less extensibility and a narrower API than Jamf, and no Windows or Android —
  it buys defaults at the price of the flexibility Jamf's exception-heavy estates need. *Present
  because it changes the answer for some fleet shapes, not because of experience with it.*

## The layer that is not a route

Client-pull software distribution and packaging automation (see
[phase 3](../phases/3-software/)) sit **underneath** whichever product is chosen. Treating
them as a third option against Jamf or Intune is a category error that shows up in a lot of
comparison writing: they answer a different question, and a specification naming both an
MDM and a packaging toolchain is describing a division of labour, not listing competitors.

## Escape Hatch

The sanctioned product blocks legitimate work — a restriction payload that also stops a real
task, an app the catalogue does not carry, a setting the profile forces the wrong way. What the
user does next is the hatch, and it is always one of three: a local-admin workaround that quietly
steps outside management, a personal device the work migrates onto (BYOD as shadow IT), or an
exception raised and waited on. The first two are the failure — an endpoint the fleet no longer
sees doing the organisation's work — and they are what a fleet gets by default when the third is
slow. The cost is not the exception; it is the unmanaged surface the *absence* of a fast exception
path creates. So the selection question hidden here is not which product blocks least, but which
one makes a **reviewed exception** cheaper to grant than to route around — an escape hatch that is
in the design (a scoped exception group, a documented override) rather than in a person's head.
