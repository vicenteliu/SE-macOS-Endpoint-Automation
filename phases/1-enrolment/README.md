# Phase 1 — Enrolment

> Sealed box to a supervised, trusted machine.

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **The ownership record** | 🔨 | How a device gets into it, and the three ways it can arrive |
| 2 | **The Setup Assistant handoff** | 🔨 | What is skippable, what is not, and waiting before the user sees a desktop |
| 3 | **Enrolment types** | 🧭 | Automated vs user-approved vs account-driven, and what each unlocks |
| 4 | **Volume ownership and escrow** | 🔨 partial | Who can unlock the disk, and whether the key comes back |

## Prerequisites

An organisational ownership record and a management server paired to it. ⛔ **Neither is available
below the full lab tier** ([tiers](../../docs/02-lab-tiers.md)) — this phase is specified and
spoken from operating one, not from a rebuilt lab.

## Hop 1 — the ownership record

A record the manufacturer honours, keyed by serial number, that answers one question at first
boot: *does anyone claim this machine?*

Three ways a device gets into it, and they are not equivalent:

- **Bought through the manufacturer or an authorised reseller** — the serial lands in the record at
  purchase. This is the only path that scales and the only one that needs nobody to remember
  anything.
- **Added afterwards with a configurator tool** — real, and the fallback for hardware that arrived
  another way. ⚠️ It typically carries a provisional window during which the person holding the
  machine can release it, which matters more than it sounds.
- **Never added.** Not an error state. See the failure section.

Inside the record, the device is **assigned to a management server**. That assignment is the entire
payload of this phase — it is what the manufacturer hands back at first boot, and everything
downstream follows from it.

## Hop 2 — the handoff

Three parties, and the order is the point:

1. **The device**, during Setup Assistant, asks whether anyone claims it.
2. **The manufacturer's service** answers with the management server the record names.
3. **The management server** receives the enrolment and begins.

⛔ **The management server never initiates.** Nothing is discovered, scanned, or pushed at a
machine that has not asked first. This is the most common misconception about zero-touch and it
inverts the trust model: **the device volunteers, because the manufacturer vouched for who owns
it.**

The enrolment profile also decides **what the person sees** — which Setup Assistant panes are
skipped, and whether enrolment is mandatory and non-removable. 🧭 *Pane configuration, and holding
Setup Assistant until the first configuration lands, are mechanism here rather than something this
document has configured.*

🔑 **This path yields supervision, and supervision is the reason the path matters.** The same
management server, on the same hardware, can do materially more when the device arrived this way.
So *"is it enrolled"* is the wrong question and *"how did it enrol"* is the right one.

## Hop 3 — enrolment types 🧭

Automated, user-approved, and account-driven enrolment differ in **what they unlock**, not in
whether a device appears in a console. A device can be enrolled and still be missing half the
management surface, and nothing about the console view says so.

⛔ Mapped, not run.

## Hop 4 — volume ownership and escrow

On current hardware, the ability to unlock and update the system volume is held by specific
accounts and by a token the management server holds. **A machine can be fully enrolled and still
have nobody who can unlock it** — the two are separate questions, and they are usually discovered
to be separate at the worst moment.

The half that matters operationally is **key escrow**: disk encryption keys held centrally, keyed
by serial, so a machine whose user cannot log in is recoverable rather than reinstalled. 🔨 *A
self-built escrow of exactly this shape — keys stored centrally, indexed by serial, and used to
recover machines — is behind this section; the specific implementation is not published
([DISCLOSURE](../../DISCLOSURE.md)).*

🥇 **The design point worth carrying: an escrow nobody has ever restored from is a backup nobody
has ever restored from.** The store is not the deliverable; the retrieval is.

## How this phase fails

**Every failure here is silent, and each one looks like success.** That is not a coincidence — the
whole phase is a machine deciding for itself whether it belongs to you, and a machine that decides
*no* still works perfectly.

- 🔴 **Missing from the record.** Setup Assistant finds no owner, hands the box to whoever is
  holding it, they make themselves an administrator, and the machine is fine. It is simply not
  yours. **Nothing alerts.** It surfaces later as a serial nobody can account for, usually when
  someone compares the estate against the record and finds they disagree.
- **No network at Setup Assistant.** No reachable service, no enrolment, and the person is through
  to the desktop. Unmanaged, and looks configured.
- **Stale assignment.** The serial is in the record but points at a retired or wrong management
  server. It enrols cleanly, somewhere nobody is looking.
- **Configuration races the person.** Without holding Setup Assistant, the desktop arrives before
  the settings do; the visible symptom is a machine that "changes by itself" for ten minutes. That
  is a support call and a first impression, not an incident.
- **Enrolled, but nobody owns the volume.** Discovered on the day a machine needs to be unlocked
  or updated, which is never a convenient day.

## Verification

| | Check | Expect |
|---|---|---|
| 1 | Reconcile the estate against the ownership record | They agree. **A serial in one and not the other is the finding this check exists for** |
| 2 | Erase a device and let it enrol | Enrolment happens during Setup Assistant, not after login |
| 2 | Inspect the enrolled record | **Supervised**, and the management profile **non-removable** |
| 3 | Compare the management surface against a user-approved enrolment | The difference is visible and expected. If it is not, the device did not enrol the way you think |
| 4 | Confirm volume ownership after enrolment | An account and a token that can actually unlock and update. Presence in a console is not this check |
| 4 | 🥇 **Take a key out of escrow and unlock a machine with it** | It works. Untested escrow is the default state and it is indistinguishable from working escrow until the day it is not |

## Acceptance

🔴 **Not "a device enrolled." That proves the transport.**

> **A machine came back.** A key was retrieved from escrow and unlocked a device whose user could
> not log in — and the estate reconciled against the ownership record with no unexplained serials
> on either side.

The first half is the restore rather than the backup; the second is the only check that catches
the failure this phase has that nothing else will report.

## Escape Hatch

Two directions, and the second is the one that gets forgotten.

**A machine that cannot enrol** needs a named path that a person can be told over the phone, and
that path has to end somewhere better than *"send it back."* Hardware arrives outside the process
in every organisation that has ever existed; the configurator route exists for exactly this, and
it should be documented before it is needed rather than rediscovered under time pressure.

⛔ **A machine that must leave management** is the harder one. A locked, non-removable enrolment is
the correct default and it means departure, transfer and sale all route through a wipe. **Decide
what that costs before setting the flag**, not on the day someone is standing at a desk with a
laptop that has to go to a different team this afternoon.
