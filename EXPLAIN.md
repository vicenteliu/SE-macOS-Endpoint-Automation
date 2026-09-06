# The same thing, without the jargon

For the people who pay for this, depend on it, or get blocked by it — and who will never open a
terminal.

> This page assumes you are busy, not that you are new. Nothing here is simplified; it is stated
> in different units.

## What this is, in one sentence

> **A new laptop comes out of its box, is switched on, and joins a network. Twenty minutes later
> the person it belongs to can start working — and nobody has touched that machine at any point.**

## Why it is worth building

The obvious argument is hours saved, and it is the weaker one.

The real argument is that **machines built by hand are not identical**, and the difference between
two machines is where support cost actually lives. Two people, same team, same laptop model, set
up three weeks apart by two different people who were both in a hurry: one of them has a setting
the other does not, and nobody knows which. Every problem after that starts with *find out what is
different about this machine*, which is the expensive part of every support conversation ever had.

**A machine that configured itself is one you can reason about.** When something breaks on it, the
question is *what changed*, not *what was it ever*. That is the return — the hours are a
side-effect.

## What has to be true for it to work

Five things, in order. Each one depends on the one before it.

1. **Someone can prove the laptop is yours.** Not the receipt — a record the manufacturer honours,
   so that when the machine is switched on it can be told who owns it.
2. **The laptop can be told what to do.** It asks, at first boot, whether anyone claims it, and
   gets an answer. Nothing is pushed at a machine that has not asked.
3. **Settings arrive before the person does.** Not after. A machine that reaches the desktop and
   *then* starts changing looks broken to the person watching it.
4. **It can prove who it is to the network.** A certificate, delivered before the machine ever
   needs it, so getting online requires no password and no help.
5. **Software arrives and stays current without anyone asking.** Including the update that
   happens while the person is using the application it updates.

## What happens when a piece of it fails

🔴 **Read the first column before the others.**

| If this breaks | Who notices | What they cannot do | Time to recover |
|---|---|---|---|
| 1 — proof of ownership | **Nobody** | Nothing. The laptop works perfectly. It is simply not yours, and nothing says so | Hours — *after* somebody finds it, which is usually an inventory months later |
| 2 — enrolment | The new person, vaguely | Reach things everyone else has; they assume that is normal for a new joiner | Hours, once someone believes them |
| 3 — settings arriving late | The new person, immediately | Get past a permission box nobody told them about | Minutes to hours. Cheap to fix, expensive in first impressions |
| 4 — network identity | The person, instantly and completely | **Anything.** No network means no email, no files, no help | 🔴 The expensive one — it usually cannot be fixed remotely, because fixing it needs the network it cannot reach |
| 5 — software distribution | **Nobody** | Nothing, yet. The update waits politely and forever | Unbounded. A machine can sit months behind and report as fine |

🥇 **Three of those five say "nobody" or "vaguely".** That is the finding, and it is the one thing
on this page worth acting on: **the failures that cost the most are the quietest**, so the money
goes into noticing, not into preventing. A system that tells you a machine has been waiting four
months is worth more than one that makes the wait less likely.

## What this does not solve

A page that lists only what works is marketing.

- **It does not make a machine secure.** It makes machines *consistent*. Those are different
  purchases and consistency is the cheaper one.
- **It does not cover machines bought outside the process.** They are exactly the ones this cannot
  see, and there is no clever fix — the process has to be the easy path or it is not the path.
- **It does not survive being routed around.** Anyone technical enough to reconfigure their own
  machine will, if the supported way is slower than the unsupported way. That is a design
  constraint, not a discipline problem.
- **It is a chain, and it reads like one.** A failure at step 4 presents as everything after it
  failing, so the first diagnosis is usually wrong.
- **It does not remove the person.** It removes the *repetition*. The judgement calls — who gets
  an exception, what stays broken until Monday, whether an update may interrupt someone
  mid-task — are still decisions somebody makes.

## How to tell whether this page worked

Not *"was that clear."* Clear and useless is the most common failure of a page like this, and it
survives every review because it does not look like a failure.

The test is one question:

> **What would you decide differently, having read this?**

An answer that names a trade-off — *spend on noticing rather than preventing*, *make the supported
path faster before making the unsupported one harder* — is the page working. *"That was clear"* is
the page failing politely.
