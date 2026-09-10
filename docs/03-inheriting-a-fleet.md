# Inheriting a fleet

The six runbooks describe how a chain is *built*. Almost nobody gets to build one. You arrive at
an estate somebody else assembled, under whatever pressure made the seat open, and the question
is not *how do I do this* but **what is actually true here** — and what you decide from it.

This page is the verification rows from the six phases, re-ordered into the sequence you run them
in when you arrive, each with the decision the answer forces. Nothing here is new; the order is
the content. It is written for the first week, on a fleet you did not build, at whatever scale it
is. No employer and no fleet appears in it, by design ([DISCLOSURE.md](../DISCLOSURE.md)).

## Three rules before the first command

1. **Read before you change.** Every row below is read-only. The first thing you change is the
   one whose answer surprised you, and not before the whole pass is done — a fix made on day one
   is made against a picture that is still wrong.
2. **The order is by cost of being wrong, not by the chain's order.** The chain runs power-on →
   ownership → enrolment → configuration → network → software → identity. Arrival runs the other
   way round on the joints that hurt most: a serial nobody owns, a key that cannot come back, a
   lock flag set years ago.
3. **"I don't know" is a real answer, and it goes in the table.** An estate where nobody can say
   what a disabled account does to an offline machine has told you something; it has not told you
   nothing.

Markers are the ones the runbooks carry: 🔨 hands-on · 🧭 mapped, not operated · ⛔ specified, not
run. They mark the *author's* footing on each row, not the row's importance.

---

## Day one — ownership, enrolment, escrow

The three rows that decide whether the fleet can be *recovered*. Everything else can wait a week;
these cannot, because they are the ones that are invisible until the day they fail.

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 1 | Reconcile the estate against the ownership record: every serial the management server knows, against every serial the ownership record holds | They agree — or **a serial in one and not the other**, which is the finding this row exists for | A serial in the ownership record and not in management is a machine that can be re-enrolled but currently is not: find it. A serial in management and not in the record is a machine that **cannot** be re-enrolled after a wipe: that is the first thing you fix, and you fix it at the record, not the device | [1 · hop 1](../phases/1-enrolment/) 🔨 |
| 2 | Find out *how* devices enrolled — on a sample, read the enrolment type and whether the management profile is removable: `profiles status -type enrollment` on the machine, and the enrolled record in the console | **Supervised, non-removable, enrolled during Setup Assistant** — or user-approved, removable, enrolled after login. Estates that grew over years usually hold both | If any part of the fleet is user-approved, half the configuration surface is silently missing on those machines and *no profile you push will change that*. Decide the re-enrolment plan before writing a single new profile, because the profile will look applied and not be | [1 · hops 2–3](../phases/1-enrolment/) 🔨 |
| 3 | 🥇 **Take a key out of escrow and unlock a machine with it.** One machine, today, on the escrow the estate actually uses | It works — or it does not, or nobody can find where the key would be | Untested escrow is the default state and it is indistinguishable from working escrow until the day it is not. If the retrieval fails, the estate cannot recover a locked machine and every other row on this page is secondary. If nobody knows *where*, you have found the same thing more cheaply | [1 · hop 4](../phases/1-enrolment/) 🔨 |
| 4 | Confirm volume ownership on the machines you touched: `fdesetup status` and `diskutil apfs listCryptoUsers /` | An account and a token that can actually unlock and update. **Presence in a console is not this check** | A machine that shows encrypted in a console and has no volume owner who can unlock it is a machine that will fail its next major update in a way the console never reports. Count them before the next OS ships | [1 · hop 4](../phases/1-enrolment/) 🔨 |

**End of day one you can say:** whether every machine is recoverable, whether every machine is
actually managed, and which serials belong to nobody. If you can say those three things, the
first day was well spent whatever else happened.

## Week one — configuration

What is *on* the machines versus what somebody once authored.

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 5 | Read back the installed profiles on a sample (`sudo profiles list`) and compare each against what the console says it sent | Byte-for-byte the intended payload set — or a profile present with a different identifier, an older payload, or one that never landed | Where they disagree, the console has been the thing being trusted. Fix the *reporting* first: a configuration you cannot read back is not a configuration, it is a memory | [2 · hop 1](../phases/2-configuration/) 🔨 |
| 6 | Find every profile marked non-removable, and ask who set the flag and why | A short list with reasons — or a long list with none | Every non-removable profile is a future wipe. Do **not** unset any of them this week. Write down, for each, what it costs to take it off one machine today; the ones with no answer are the ones that will block someone at a desk one afternoon | [2 · Escape Hatch](../phases/2-configuration/) 🔨 |
| 7 | For the largest scopes, take the count the scope reports and enumerate its members | The two agree — or they do not, and nothing logged it | A dynamic group is a query, and nobody re-reads the query. Where count and members disagree, the count was being trusted; find what membership actually keyed on before you point anything new at that group | [2 · hop 4](../phases/2-configuration/) 🔨 |
| 8 | If any machine is on OS 27 or later, exercise one legacy software-update deferral and read what your compliance reporting says afterwards | It does not take effect. If the report still shows it applied, the report is wrong | The estate's update model is on a clock. Decide the migration to declarative management from the row that just lied to you, not from a vendor calendar | [2 · hop 2](../phases/2-configuration/) 🧭 |

## Week one — network

Ask the network team for the RADIUS side; these rows are what you can see from the endpoint.

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 9 | Inspect the network profile before it installs: does the network payload's certificate reference resolve to the identity payload's identifier? | It does — or it is empty, or it points at a different identifier | An unbound identity means machines prompt to choose a certificate, and a population that can read the prompt will pick anything that works. Fix the binding in the profile; do not train people to click through | [4 · hop 2](../phases/4-network-access/) ⛔ |
| 10 | On an enrolled machine, inspect the system keychain for the client identity and read its expiry | Present, with its private key, issued by the pinned root, expiring on a date — or absent, or expiring soon across a whole cohort | Expiry is the deadlock: a certificate that expires cannot reach the management server that would renew it. **Sort the fleet by expiry date this week.** A cohort expiring together is an outage with a date on it | [4 · hop 2](../phases/4-network-access/) ⛔ |
| 11 | Ask what happens to a machine that fails authentication, and where it lands | A named path — a quarantine segment that can still reach the management server, a wired bypass, a guest network with an onboarding page — or a shrug | If the failure path cannot reach the management server, renewal is impossible from inside the deadlock. That is a design change, and it belongs to the network team; your job is to bring them the row, not a theory | [4 · Escape Hatch](../phases/4-network-access/) ⛔ |

## Week one — software

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 12 | From a managed machine, reach the software repository the client is configured for, and read the catalogue it is actually served | Reachable, and the catalogue names what you expect — or it points at a host nobody remembers | The repository is a web server and the client decides; if the client is pointed somewhere stale, every machine is quietly making its own decisions from old metadata | [3 · hop 1](../phases/3-software/) 🔨 lab |
| 13 | Run one client check with an application open that has a pending update, then read the log | The download completes **and then** the install is refused because the application is running | This is the model working. If instead the application was replaced under the user, the blocking metadata is missing and the estate has been relying on luck. Decide which items need it before the next major version of anything | [3 · hop 2](../phases/3-software/) 🔨 lab |
| 14 | Read the packaging automation's trust state: are recipe overrides pinned, and does a run verify a signature? | Pinned, and a signature verification appears in the run — or overrides are unpinned and nobody has looked at a recipe change in a year | Unpinned automation is a supply chain with no gate; the fix is cheap and the exposure is the whole fleet. It goes near the top of week two | [3 · hop 3](../phases/3-software/) 🔨 lab |

## Week one — identity, only if the estate attaches machines to a directory

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 15 | Log in on a machine with the identity provider unreachable | A stated, intended outcome — or a discovery | If it is a discovery, it becomes a documented outcome this week, whichever way it went | [5 · hop 1](../phases/5-identity-optional/) 🧭 |
| 16 | Enumerate the endpoints unmanaged devices reach, and which authority signed each | Every one publicly trusted — or **an internal authority on one of them**, which is the finding | A private root on an endpoint unmanaged devices reach is a control that is already being bypassed by everyone who could not install the root. Decide whether the endpoint or the trust boundary moves | [5 · hop 2](../phases/5-identity-optional/) 🔨 |
| 17 | Find the local account that exists when the directory does not, and confirm somebody can use it | It exists, it is documented, it rotates — or it is the same credential everywhere, or it is absent | Absent is a hole in survivability; identical everywhere is a hole in security. Both get fixed, and the second one first | [5 · Escape Hatch](../phases/5-identity-optional/) 🔨 |

## Week two — operations, read from the queue's own data

| # | Run | The answer looks like | What you decide from it | From |
|---|---|---|---|---|
| 18 | Count P0s over the last twelve months, and sample where open incidents sit | A handful of P0s and a queue mostly at P2 — or a monthly P0 and a queue that is mostly P1 | The second estate has a decorative severity scheme: nothing in it means anything, including the escalations. Re-baseline severity before touching the escalation path | [6 · hop 1](../phases/6-operations/) 🔨 |
| 19 | Ask the queue what recurred more than five times this quarter | An answer from the data — or an answer from a person remembering | If it takes a person, the queue is not memory. The recurring item, whatever it is, is the first engineering target: the acceptance criterion for operations is a queue that got smaller for a reason somebody can name | [6 · hop 1](../phases/6-operations/) 🔨 |
| 20 | Trace the last five escalations | One hop each — or three | Three hops means the escalation path is theoretical and the real one is a back channel. Do not close the back channel; make it cheap to log, and watch the ratio | [6 · Escape Hatch](../phases/6-operations/) 🔨 |

---

## What this pass is accepted on

> **For every hop of the chain you can say whether it is true on this estate, from something you
> read rather than something you were told — and the first change you make is the one whose answer
> surprised you.**

Not *"the fleet is healthy."* Nobody can say that in a week, and the estates where someone does are
the ones where row 3 has never been run.

## What is deliberately not here

- **No fixes.** Every row reads; none changes. The runbooks say how to change things, once the
  picture is right.
- **No timeline shorter than a week.** A day-one *fix* is the most expensive kind of wrong.
- **No 30-60-90 plan.** The document a hiring manager asks for is a derivative of this page,
  written for one organisation, and it names that organisation — so it is never published here.
