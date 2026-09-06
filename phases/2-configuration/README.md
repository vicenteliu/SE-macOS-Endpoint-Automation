# Phase 2 — Configuration

> Trust to a machine that behaves.

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **Configuration profiles** | 🔨 bounded | Payload structure, scope, signing, removability — from inside the file, not only the console |
| 2 | 🥇 **Declarative management** | 🧭 | What is actually changing in 2026, and what stops working |
| 3 | **Privacy pre-authorisation** | 🧭 | Why an automated tool must be granted access before it asks. 🚧 *Stays a ramp: the profile work in row 1 does not extend to TCC/PPPC* |
| 4 | **Scoping** | 🔨 bounded | Dynamic grouping and device-reported attributes — and why scope drift is the failure mode nobody instruments |

## Prerequisites

An enrolled, supervised device ([phase 1](../1-enrolment/)). ⛔ Nothing in this phase applies to a
machine that has not enrolled — the whole surface exists because the device asked first.

## Hop 1 — what a profile actually is

An XML property list. One top-level dictionary carrying metadata — identifier, UUID, organisation,
removability — and inside it an **array of payloads**, each configuring exactly one subsystem.

🔑 **The unit is the payload, not the file.** One profile can carry several, which is how a network
payload and the certificate it depends on arrive together and in the right order
([phase 4](../4-network-access/)).

Four mechanics worth knowing before touching one:

- **Identity.** Installing a profile whose `PayloadIdentifier` already exists **replaces** the
  existing one. That is the update mechanism, and it is also the accident: two teams shipping the
  same identifier means the second silently takes ownership of the first's settings. Nothing errors.
- **Signing.** A profile can carry a CMS signature. Signed displays as verified, unsigned as
  unverified — a real difference for anything a person sees.
  ⚠️ **Signing has a second, less obvious effect**: management consoles have been reported to
  rewrite imported custom profiles to fit their own internal payload structure — putting back keys
  that were deliberately removed, dropping values they do not recognise. Signing before upload
  prevents that, at the cost of no longer being editable in the console. **Verify what landed on
  the device rather than trusting what was uploaded.**
- **Removability.** A profile can be locked so it cannot be removed without a wipe. Cheap to
  decide, expensive to reverse — see the Escape Hatch.
- **Scope.** Payloads apply at device or user level. A user-level setting does not follow the next
  person who logs in, which is the usual explanation for *"it works on my account."*

## Hop 2 — 🥇 what is actually changing, as of 2026-09

⚠️ **Dated deliberately.** This is the section of this repository most likely to age, and a page
that states this early reads differently from one that states it late.

**Configuration profiles are not being removed. They are being subsumed.** Declarative device
management is the delivery and enforcement model; from **OS 27.0** a legacy profile can be
delivered *as a declarative asset* — carried by a configuration that references it rather than
installed by a command.

🔴 **What genuinely stops working is narrower and harder.** Apple's own wording: *legacy software
update management no longer functions in all 27.0 operating systems* — the software update
**commands**, **queries**, **recommended cadence settings**, and **restrictions including
deferrals**. Declarative software update management is the stated replacement.

**So the accurate sentence is** *"profiles are the payload format; declarative management is the
delivery and enforcement model"* — **not** *"profiles are deprecated."* The second is a common
thing to say in 2026 and it is wrong in a way that is easy to check.

### How this fails

🥇 **An estate does not notice.** Update deferrals and enforcement built on the legacy commands
stop functioning as machines take 27.0, and the compliance posture changes **without anyone
changing anything**. There is no migration event to schedule around — the mechanism simply stops
being a mechanism.

⚠️ Whether a management server surfaces an error or the command is silently inert is **not
verified here**. The sourced fact is that it no longer functions.

Adjacent, same direction: the managed content-caching profile is deprecated in macOS 27 in favour
of a declarative configuration, and restriction keys covering Apple Intelligence, Siri and
keyboard settings were deprecated in the 26.4 releases.

## Hop 3 — privacy pre-authorisation 🧭

An automated tool that needs access to files, the screen, or another application must be **granted
that access before it asks**, or it gets a dialog the automation cannot answer. That grant is
itself a payload, and it only holds on a device that enrolled the right way.

⛔ **Mapped, not run.** The profile work above does not extend here, and this section says what the
mechanism is for rather than how to operate it.

## Hop 4 — scoping, and the failure nobody instruments

Membership is computed from what devices report about themselves, so **a scope is a query, not a
list**. That is what makes it scale and what makes it drift: the set changes when the estate
changes, and nothing announces that it has.

🔴 **The console tells you a policy reaches three machines. It reaches twenty-two.** Nobody is
alerted, because from the system's point of view nothing went wrong — the query returned what the
query returns.

A runnable demonstration of exactly this failure is in the author's other public repository:
[`sysadmin-self-cultivation` → endpoint labs → `policy-blast-radius`](https://github.com/vicenteliu/sysadmin-self-cultivation).

## Verification

| | Check | Expect |
|---|---|---|
| 1 | Read back the installed profiles on the device | The profile present with the expected identifier |
| 1 | Install a second profile carrying the **same** identifier | **One** profile afterwards, not two — carrying the second one's content |
| 1 | Compare what was uploaded with what landed on the device | Byte-for-byte the intended payload set. ⚠️ This check exists because the answer is not always yes |
| 2 | On a 27.0 machine, exercise a legacy software-update deferral | It does not take effect. If your compliance reporting still shows it applied, the reporting is the thing to fix first |
| 4 | Take the count a scope reports, then enumerate the members | The two agree. When they do not, the count was the thing being trusted |

## Acceptance

A profile installs, replaces cleanly on a second install with the same identifier, and **what is on
the device matches what was authored**. ⛔ Not yet demonstrated end to end here — hop 1 is
hands-on, hops 2 and 3 are mapped, and the verification table above is the specification for
closing that.

## Escape Hatch

🔑 **The lock flag is where this phase blocks people, and it is set long before anyone finds out.**

- **Lock only what must be locked.** Non-removable is the right answer for the enrolment profile
  and for controls with a compliance obligation behind them. Applied by default, it turns every
  future exception into a wipe.
- **Know the exit before setting the flag.** *"What does it cost to take this off one machine
  today"* is a question with a cheap answer or an expensive one, and it is answered at authoring
  time whether or not anyone asks it.
- **A blocked person needs a named path**, not a ticket queue. If the sanctioned route to an
  exception is slower than a workaround, the workaround wins — and an undocumented workaround is
  the outcome this phase exists to avoid.
- ⛔ **Do not use a locked profile to enforce something a conversation should settle.** On a
  population that can read the payload, a lock is an opening argument, not a conclusion.
