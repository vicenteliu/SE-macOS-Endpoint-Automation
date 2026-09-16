# Troubleshooting — symptom first, and where the boundary sits

[docs/03](03-inheriting-a-fleet.md) is arrival-first: *what is actually true on this estate.*
This page is symptom-first: *something is broken now — what do I read, what does it mean, what do
I decide, and what fixes it.* Same chain, entered from the other end.

Nothing here is a new claim. Every **Read** cell is a read-only command the phases and docs/03
already carry; every symptom links to the phase it comes from and carries that phase's footing
(🔨 hands-on · 🧭 mapped, not operated · ⛔ specified, not run). What this page adds is the order
a fault is worked in and, on every remediation, **who is allowed to do it** — because that is the
line this repository exists to draw, and a fault is where it gets crossed under pressure.

No employer and no fleet appears here, by design ([DISCLOSURE.md](../DISCLOSURE.md)).

## Three rules before the first change

1. **Diagnose read-only before you change anything.** Every **Read** below changes nothing. The
   first thing you change is the one the reads point at, made *after* the pass, not during it — a
   fix made on a picture that is still forming is how one fault becomes two.
2. **The boundary is the cost of being wrong, not the difficulty.** A reversible or read-only step
   is 🤖 — a script or an agent can do it unattended. An irreversible or blast-radius step is 🔴 —
   a person does it, because *reimage it* and *unset that profile* are exactly the fast advice that
   is wrong on the one machine it is wrong on. The line is drawn by what it costs if it is wrong on
   *this* device, never by how hard the command is to type.
3. **A symptom with no reproduction is a report, not a fault.** *"It's slow", "it keeps dropping"*
   are triaged by turning them into a command that returns a number or a log line. If nothing
   read-only reproduces it, that is itself the finding, and it goes in the record — you have not
   found nothing.

## The markers in the Remediate column

| | Means |
|---|---|
| 🤖 | Read-only, reversible, or collect-only. A script, an MDM command, or an agent can do it unattended — and the [ledger](../AGENT_BOUNDARY.md) says which of these have been handed to a model. |
| 🔴 | Irreversible or blast-radius: a wipe, an unenrolment, an unlock, unsetting a non-removable profile, a promotion to production, a reboot of a cohort. A person acts; automation may *propose* and never execute. |
| 🔑 | The thing most people get wrong here. |

---

## A · A device stopped being managed

The commands that were pushed are not landing; the console may still show the device as enrolled.

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| On the device: `profiles status -type enrollment` | `An enrollment profile is currently installed` with an MDM URL — or none, or one that is *user-approved* and removable | Whether this device is actually under management or only appears to be. 🔑 *"Is it enrolled"* is the wrong question; *"how did it enrol"* is the right one — supervised and non-removable, or user-approved and gone the day someone removed the profile | 🤖 re-run the check across the sample and classify each result; 🤖 send the management server's *device information* / blank-push command to prompt a check-in — reversible, it asks nothing of the user. 🔴 **re-enrolment** (which for supervision means Setup Assistant, i.e. a wipe) is a person's call, per device | [1 · hops 2–3](../phases/1-enrolment/) 🔨 |
| The device record from the management server's API, next to the on-device answer | They agree — or the console believes it can manage a device that no longer holds the profile | Which one to trust. The device is the ground truth; the console is a memory of the last check-in | 🤖 reconcile the two lists and produce the disagreements ([ledger I.1](../AGENT_BOUNDARY.md), run against three models); 🔴 what is *done* about a device in one and not the other is the decision the ledger keeps with a person | [1 · hop 1](../phases/1-enrolment/) · docs/03 row 1 🔨 |

## B · A profile is applied in the console but its setting is not in effect

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| `sudo profiles list`, then `sudo profiles show -output stdout-xml` for the payload in question | The payload is present byte-for-byte — or a different identifier, an older payload, or absent while the console says *installed* | Where they disagree, the console has been the thing trusted. A configuration you cannot read back on the device is not a configuration, it is a memory | 🤖 read back the installed profiles across the sample and diff each against what the console sent; 🤖 **re-push** the profile (reversible — the payload replaces itself) | [2 · hop 1](../phases/2-configuration/) · docs/03 row 5 🔨 |
| Two profiles that set the same domain: compare their `PayloadIdentifier`s and payload keys | An identifier collision — two profiles fighting over one setting, last-writer-wins, and neither console view shows the loser | Which profile owns the setting, and which is the accident | 🤖 enumerate the profiles touching the domain and show the collision; 🔴 removing or renarrowing a profile scope is a change with a blast radius — a person decides which one goes | [2 · hop 4](../phases/2-configuration/) 🔨 |
| For a payload that will not remove: is it marked non-removable, and by whom | A non-removable profile is a future wipe if its removal is ever needed and the enrolment cannot re-push it | Do **not** unset it to fix today's symptom | 🤖 list every non-removable profile with the cost of removing one today; 🔴 unsetting non-removable is 🔴 always — it is a witnessed, per-machine act | [2 · Escape Hatch](../phases/2-configuration/) 🔨 |

## C · A machine cannot be recovered — FileVault and escrow

The symptoms that are invisible until the day they are not: a locked machine, a failed major
update, a key that will not come back.

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| `fdesetup status`; `diskutil apfs listCryptoUsers /` | Encrypted, with an account and a secure token that can actually unlock and update — or encrypted with no volume owner who can | 🔑 **Presence in a console is not this check.** A machine that shows encrypted in the console and has no unlockable volume owner will fail its next major update in a way the console never reports | 🤖 confirm volume ownership across the machines touched, and count the ones with no owner *before* the next OS ships; 🔴 adding a volume owner / secure token touches account state on the machine — a person | [1 · hop 4](../phases/1-enrolment/) · docs/03 row 4 🔨 |
| Take a key **out of escrow** and unlock one machine with it, today, on the escrow the estate actually uses | It works — or it does not, or nobody can find where the key would be | Untested escrow is indistinguishable from working escrow until the day it is not | 🤖 list the machines whose record *claims* an escrowed key (the read); 🔴 **the retrieval and the unlock are witnessed** — an unlock a script *reports* is exactly the untested escrow this row exists to catch. The [ledger marks it ⛔](../AGENT_BOUNDARY.md) for the same reason | [1 · hop 4](../phases/1-enrolment/) · docs/03 row 3 🔨 |

## D · An app will not update, or clients are on stale software

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| From a managed machine: `curl -so /dev/null -w '%{http_code}' http://<repo>/catalogs/<catalog>` → **200**; the directory itself → **403** | The catalogue the client is configured for is reachable and served — or the client points at a host nobody remembers | The repository is a web server and the client decides; a client on stale metadata is quietly making its own decisions | 🤖 reach the repository and read back the catalogue the client is served; 🤖 re-point the client's catalogue (reversible config) | [3 · hop 1](../phases/3-software/) 🔨 lab |
| Run a client check with the target application **open**, then read `log show --predicate` for the run | The download completes **and then** the install is refused because the application is running (`Blocking apps ... are running`) | 🔑 This is the model *working*. If instead the app was replaced under the user, the blocking metadata is missing and the estate has been relying on luck | 🤖 re-run the client check and read the log; 🤖 propose the blocking array from the app bundle *as a diff*; 🔴 the blocking array that decides when a running app is refused is a decision — a person approves the diff (ledger 3.2) | [3 · hop 2](../phases/3-software/) 🔨 lab |
| The packaging automation's trust state: are recipe overrides pinned, and does a run show a passed signature verification? `autopkg run … --report-plist` and the signature step in it | Pinned, with a verification in the run — or overrides unpinned and no one has looked at a recipe change in a year | Unpinned automation is a supply chain with no gate; the exposure is the whole fleet | 🤖 run the processor chain and read the signature step back; 🔴 **re-pinning trust after a changed parent recipe** stays with a person — accepting an upstream change is not the automation's call (ledger 3.3, held by three models) | [3 · hop 3](../phases/3-software/) 🔨 lab |
| For a testing item that should be live: the catalogue and manifest diff | The item is in `testing`, not `production` — nothing reached the clients because nothing was promoted | Promotion is the release | 🤖 produce the diff of what would change and the count of clients the manifest reaches; 🔴 **the promotion is 🔴** — the ledger marks 3.4 ⛔ for exactly this | [3 · hop 2](../phases/3-software/) 🔨 lab |

## E · A cohort fell off the network

⚠️ These rows are 4's — the phase that is **specified, not run** ([docs/01 / ADR-0001](adr/0001-specced-not-run-is-a-third-marker.md)). The reads are what an endpoint can show; the RADIUS side belongs to the network team.

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| On an enrolled machine: the system keychain for the client identity and its expiry | Present, with its private key, issued by the pinned root, expiring on a date — or absent, or expiring soon across a whole cohort | 🔑 **Expiry is the deadlock**: a certificate that expires cannot reach the management server that would renew it. A cohort expiring together is an outage with a date on it | 🤖 read expiry across the fleet and **sort by date this week** — the whole remediation is seeing it coming; 🔴 forcing a renewal path for a cohort already past expiry is a design change, and it belongs to the network team | [4 · hop 2](../phases/4-network-access/) ⛔ |
| Inspect the network profile before it installs: does its certificate reference resolve to the identity payload's identifier? | It resolves — or it is empty, or points at a different identifier | An unbound identity means machines prompt to choose a certificate, and a population that can read the prompt picks anything that works | 🤖 read the binding in the profile before it ships; 🔴 fixing the binding and re-issuing is a profile change with a blast radius | [4 · hop 2](../phases/4-network-access/) ⛔ |
| Ask what happens to a machine that fails authentication, and where it lands | A named path — a quarantine that can still reach the management server, a wired bypass — or a shrug | If the failure path cannot reach the management server, renewal is impossible from inside the deadlock | 🔴 this is a network-team design decision; your job is to bring them the row, not a theory | [4 · Escape Hatch](../phases/4-network-access/) ⛔ |

## F · Login fails when the directory is unreachable

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| Log in on a machine with the identity provider unreachable, on a test account | A stated, intended outcome — or a discovery | If it is a discovery, it becomes a documented outcome this week, whichever way it went | 🤖 reproduce it on a test machine and record the outcome; 🔴 changing the mobile-account / cached-credential policy is a fleet decision | [5 · hop 1](../phases/5-identity-optional/) 🧭 |
| Find the local account that exists when the directory does not, and confirm someone can use it | It exists, is documented, rotates — or is the same credential everywhere, or is absent | Absent is a hole in survivability; identical everywhere is a hole in security | 🔴 both get fixed, and the second first — a break-glass credential is a person's to hold and rotate | [5 · Escape Hatch](../phases/5-identity-optional/) 🔨 |

## G · The same fault keeps coming back

| Read | What it means | Decide | Remediate | From |
|---|---|---|---|---|
| Ask the queue what recurred more than five times this quarter — from the data, not from a person remembering | An answer from the queue — or an answer only a person can give | 🥇 If it takes a person, the queue is not memory, it is a logging system with a ticket number. The recurring fault, whatever it is, is the first engineering target | 🤖 read the recurrence from the queue's own data and rank it; 🔴 deciding which recurrence to *engineer away* is a person's call — it trades triage time for a fix | [6 · hop 1](../phases/6-operations/) 🔨 |
| Count P0s over the last twelve months; sample where open incidents sit | A handful of P0s and a queue mostly at P2 — or a monthly P0 and a queue mostly at P1 | 🔑 A monthly P0 is not a severity level, it is a synonym for *important to me*; the severity scheme has stopped carrying information | 🤖 read the counts; 🔴 **assigning severity, and re-baselining it, is a person's** — automation proposes the number from blast radius and reversibility, never sets it | [6 · hop 1](../phases/6-operations/) 🔨 |

---

## The automation, stated once — and its edges

What a script or an agent does unattended, and where every human gate sits. This is the honest
shape of it: the automation this repository has run is **client-pull distribution (Munki) and
packaging automation (AutoPkg)**, plus the read-only diagnosis and reconciliation the
[ledger](../AGENT_BOUNDARY.md) has handed to models. There is no self-healing here that has not
been built; a remediation that automates is one that is read-only, reversible, or collect-only.

- **🤖 Collect.** A fixed, read-only command set run on a symptomatic host and returned — the
  device's enrolment state, its profiles, its FileVault status, its catalogue reachability, its
  certificate expiry. This is the diagnostic bundle ([ledger T.1](../AGENT_BOUNDARY.md)); the
  *sending* of it anywhere is a person's act, because it carries configuration and logs.
- **🤖 Reconcile and classify.** Diff the device against the console (I.1); name the probable
  cause from the read-only outputs with the evidence line (T.2). The output is a recommendation.
- **🤖 Re-apply the reversible.** Re-push a profile, re-point a catalogue, re-run a Munki check,
  re-run the AutoPkg chain — each replaces state with the same state or a config that can be put
  back.
- **🔴 The gate is everything irreversible or wide.** Re-enrolment/wipe, unsetting a non-removable
  profile, the escrow unlock, re-pinning trust after an upstream change, promotion to production,
  a cohort renewal or reboot, and *assigning a severity*. Automation may prepare the diff and name
  the command; a person runs it.

The rule underneath all of it is the repository's: **the line is the cost of being wrong on this
machine, not the difficulty of the command.** A password reset is safe everywhere and automates;
*reimage it* is the fast advice that is wrong on the one machine it is wrong on, and it does not.

### The flow, wired end to end (a demonstration)

The edges above are a pipeline, and its last stage is a wall:

```
  collect ──▶ classify ──▶ propose ──▶ │ GATE │
   🤖 read-only  🤖 a model   🤖 name the   🔴 a person decides
   diagnostics   names the    remediation   and runs it; severity
   → a bundle    cause + the  from docs/05  and the trigger stay
   (T.1)         evidence     with 🤖/🔴    a person's (T.3, ⛔)
                 line (T.2)   marks
```

[`lab/triage.sh`](../lab/triage.sh) runs it, and [`lab/triage.out`](../lab/triage.out) is a run on
the T.1/T.2 fixture: it **collects** the read-only captures into a bundle (and says it is *not sent*
— that is a person's act), **classifies** them with the local model — *"the USB-restriction
profile the server records as deployed is absent from the device (console-record vs profiles-list)"*
— **proposes** symptom B's remediation with its marks (🤖 re-push the profile and re-check;
🔴 do not unset a non-removable profile, and re-enrolment on a supervised Mac is a wipe), and then
**stops**. Nothing on the host changed; a person decides from the gate.

It wires the pieces this repository already has — [`verify.sh`](../lab/verify.sh) is the collect
stage against a real host, [`run.py`](../lab/agent/run.py) is the classify model call, and this
page's symptom tables are the propose lookup. It is a thinking aid and a demo, not a product: the
value is that the automation **runs up to the gate and no further**, which is the same boundary the
[ledger](../AGENT_BOUNDARY.md) draws (T.1 collect · T.2 classify · T.3 ⛔ decide). On a real fleet
the collect stage points at the host and the classify stage can be any model; the gate does not
move.

## What AI can assist, and what a person decides

Per responsibility, with the model and the date on every row that was actually tried, in
[AGENT_BOUNDARY.md](../AGENT_BOUNDARY.md) — its **Troubleshooting** section carries the three
that belong to this page: collecting the diagnostic bundle (T.1), classifying a symptom to a
probable cause (T.2), and deciding severity and triggering the remediation (T.3, ⛔ — the person).

## Acceptance

> **For any live symptom, the fault is worked read-only to a probable cause traceable to a
> command's output, the remediation names who is allowed to run it, and the first change made is
> the one the reads pointed at — not the fast one.**

Not *"the fleet is healthy."* A page that lets someone skip the read and jump to the reimage has
made the estate worse, not better.

## What is deliberately not here

- **No self-healing that was not built.** Every 🤖 step is read-only, reversible, or collect-only;
  nothing here claims an estate that fixes itself, because this author has not run one.
- **No symptom without a read.** A row with a remediation and no read-only diagnosis in front of
  it is not on this page.
- **No employer, no fleet, no reconstructible incident** ([DISCLOSURE.md](../DISCLOSURE.md)).
