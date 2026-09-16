# Verification audit — which rows have a command, which need one, which cannot have one

ADR-0002 says a verification row is a command or an API call plus its expected output. This is
the audit of the rows that existed before that rule, taken **as written** on 2026-09-15. Nothing
was changed to pass it. Each row that failed became a hop when it was turned into a command. **2026-09-16: the sixteen
🔧 rows were resolved in one pass** — each now names its command and expected output in its phase's
Verification table, with the tier that produces it; the classes below are updated to ✅. What a
named command *returns on a real machine* (seen vs specified by tier) is the separate job of
`verify.sh` ([TODO.md](../TODO.md) item 4), for the minimum-tier rows only.

| Class | Means |
|---|---|
| ✅ command | The row names a command or an API call and what it returns. |
| 🔧 command exists | The row names a check; a command or API call can produce it, and the row says which. Debt. |
| ⚠️ GUI-only | No command or API produces this. The row stays, marked, with the reason. |
| 👁 witnessed | The check is a physical act a person performs. Not a GUI row and not a debt; a command cannot replace it. |

## Phase 1 — enrolment

| Row | As written | Class | Command or reason |
|---|---|---|---|
| 1 | Reconcile the estate against the ownership record | ✅ | Management server API for the device list; the ownership record's API where the vendor exposes one, its export where it does not. Diff the serial sets. |
| 2 | Erase a device and let it enrol | 👁 | Setup Assistant is the point of the row. The *result* is checkable: row 2b. |
| 2 | Inspect the enrolled record | ✅ | `profiles status -type enrollment` on the machine; the device record from the management server's API. Both, because the row's finding is a disagreement between them. |
| 3 | Compare the management surface against a user-approved enrolment | ✅ | `profiles status -type enrollment` on one machine of each kind; the management server's API for what it believes it can do to each. |
| 4 | Confirm volume ownership after enrolment | ✅ | `fdesetup status`; `diskutil apfs listCryptoUsers /` — already in docs/03 row 4. |
| 4 | Take a key out of escrow and unlock a machine with it | 👁 | Retrieving the key is an API call; the unlock is the witnessed act. The ledger marks it ⛔ for the same reason. |

## Phase 2 — configuration

| Row | As written | Class | Command or reason |
|---|---|---|---|
| 1 | Read back the installed profiles on the device | ✅ | `sudo profiles list` — in docs/03 row 5. |
| 1 | Install a second profile carrying the same identifier | ✅ | Push the second profile through the management server's API (its install-profile command) — `profiles install` cannot install configuration profiles on current releases — then `sudo profiles list`; count the identifier. |
| 1 | Compare what was uploaded with what landed | ✅ | The profile body from the management server's API; `sudo profiles show -output stdout-xml` on the machine; diff the payload sets. |
| 2 | Exercise a legacy software-update deferral on a current release | ✅ | Install the profile, then `sudo softwareupdate --list` and the update-related keys from `defaults read`; the row's expected result is *no effect*. Tier: one machine on the current release. |
| 4 | Take the count a scope reports, then enumerate the members | ✅ | The management server's API: the scope object's count, then its member list. The row exists because these disagree. |

## Phase 3 — software distribution

All five rows ✅ — command and expected output, run on the minimum tier. The only phase that
passed the rule before the rule existed, which is the reason it was written first.

## Phase 4 — network access

No verification table: ⛔ Specced-Not-Run (ADR-0001). The specification names the tier that
could produce each check; it is not in this audit until a tier exists.

## Phase 5 — identity, optional

| Row | As written | Class | Command or reason |
|---|---|---|---|
| 1 | Log in with the identity provider unreachable | ✅ | Block the provider's endpoints at the host firewall (`pfctl` with a scoped anchor), attempt login, read the outcome from `log show --predicate` on the authorization subsystem. Tier: one machine bound to a test directory. |
| 2 | Enumerate endpoints reached by unmanaged devices | ✅ | The gateway or DNS resolver's query log for a sample of unmanaged clients; `openssl s_client -connect` per endpoint for the issuing authority. |
| 2 | Enumerate endpoints reached only by managed devices | ✅ | Same as above, filtered to managed clients. |
| 3 | Change a password in the directory, then log in | ✅ | The directory's API for the change; login outcome from the authorization log. Tier: a test directory. |
| 3 | Disable an account, then attempt login offline | ✅ | The directory's API to disable; login attempt with the provider blocked as in row 1. |

## Phase 6 — operations

| Row | As written | Class | Command or reason |
|---|---|---|---|
| 1 | Count P0s over twelve months | ✅ | The ticket system's query API, filtered by severity and date. |
| 1 | Sample open incidents and read their severity | ✅ | Same API, open state, grouped by severity. |
| 1 | Ask the queue what recurred more than five times | ✅ | Same API, grouped by category or linked problem; the row's point is that the answer must come from the data. |
| 1 | Trace the last five escalations | ✅ | The ticket system's audit trail per ticket; count assignment hops. |
| 3 | Give `EXPLAIN.md` to someone outside the domain | 👁 | A human reading. Not a command by design. |

## Rows in docs/03 not covered above

docs/03 re-orders the rows above; rows 2, 4 and 5 there already carry their command. The rest
inherit the class from the phase they came from.

## Count

✅ 23 · 🔧 **0** · ⚠️ GUI-only **0** · 👁 3

Nothing in this chain is GUI-only, and as of 2026-09-16 nothing is 🔧 either: every check now
names a command or an API call and what it returns, in its phase's Verification table. The
minimum-tier rows now also have *what they returned on a real machine*: [`lab/verify.sh`](../lab/verify.sh)
ran the phase 1/2/3 read-only checks once ([`lab/verify.out`](../lab/verify.out), 2026-09-16) on an
**unmanaged** reference Mac — so the enrolment and profile rows carry their honest *not-enrolled /
none* outputs, and phase 3 reproduced `403`/`200`. The mid/full-tier rows name the tier and wait
for it, the same way phase 4 waits ([ADR-0001](adr/0001-specced-not-run-is-a-third-marker.md)).
The three 👁 rows are witnessed acts a command cannot replace, by design.
