# Agent Boundary Ledger

Where, in this chain, a model is allowed to act, and where a person decides — one row per
responsibility, and a **model line** on every row that was actually tried, because the boundary
moves as models change and a boundary with no date on it is an opinion.

**Rules** (ADR-0002):

- A row is a **Responsibility Item**: one duty concrete enough that the line through it can be
  drawn and argued. Rows come from this repository's own runbooks and from
  [docs/03](docs/03-inheriting-a-fleet.md); nothing here was invented for the ledger.
- **Human decides** / **Agent executes** / **How** / **How you know it worked** are the four lines
  every row carries. The fourth is an **Acceptance** — a command or an API call and what it must
  return — never a feeling that it worked.
- **Model** is the exact identifier that ran, and where: `anthropic:<id>`, `openai:<id>`,
  `ollama:<id>@<host>`, `lmstudio:<id>@<host>`. **Tested on** is the date. One row per model
  tried; when a model generation changes the old row stays and a new one is added, so the ledger
  is a history of the boundary moving, not a snapshot.
- Only a model that **actually ran** the task gets a model line. A model read about is not a
  model tried.
- Every 🔨 row points at a file in [`lab/agent-runs/`](lab/agent-runs/) — the command, the
  model, the transcript, the pass/fail against the acceptance. That file is the evidence; a row
  without one is 🧭 no matter what it says.

**Status**:

| | Means |
|---|---|
| 🔨 | An agent ran it against the acceptance, and the run is in `lab/agent-runs/`. |
| 🧭 | The line is drawn by judgement. Nobody has handed this to a model yet. |
| ⛔ | Deliberately not handed to a model, with the reason in the row. |
| ⏳ | The model line is stale: the generation changed, or it is more than 90 days old. Re-run before citing. |

---

## Phase 3 — software distribution

| # | Responsibility | Human decides | Agent executes | How | How you know it worked | Model | Tested on | Status | Run |
|---|---|---|---|---|---|---|---|---|---|
| 3.1 | Publish the repository over HTTP | Whether the repository is reachable beyond one machine, and whether it needs authentication | The web-root symlink and the two reachability checks | Shell on the repository host | `curl -so /dev/null -w '%{http_code}' http://localhost/<repo>/catalogs/<catalog>` → **200**; the directory itself → **403** | | | 🧭 | |
| 3.2 | Import a vendor package and derive its version-comparison and blocking metadata | The catalog it lands in, and whether the derived blocking list is right — the array that decides when a running application is refused is a decision, not a field | The import, the metadata read-back, and a proposed blocking list from the application bundle | Client tooling on the repository host; the proposed array shown as a diff | Client run **with the application open** → `Blocking apps ... are running` after the download line; run with it closed → `Install of <app>-<newer>: SUCCESSFUL` | | | 🧭 | |
| 3.3 | Author a recipe override and run the processor chain | Which parent recipes are trusted. A changed parent recipe is a supply-chain event, and the trust decision never moves to the thing being trusted | Create the override from the parent, run the chain, read the signature-verification step back | Packaging automation on the repository host | The full processor chain in the run output, with a passed signature verification inside it; a **failed** trust check stops the run and is reported, not overridden | | | 🧭 | |
| 3.4 | Promote an item from the testing catalog to production | Always. This is the release decision | The diff of what changes and the count of clients the manifest would reach — the report, not the promotion | Catalog and manifest read-back | The report names the item, the version delta and the manifest scope, and the promotion has **not** happened until a person runs it | | | ⛔ — the release decision stays with a person by design, not because a model cannot edit a catalog | |

## Inheriting a fleet — day one ([docs/03](docs/03-inheriting-a-fleet.md))

| # | Responsibility | Human decides | Agent executes | How | How you know it worked | Model | Tested on | Status | Run |
|---|---|---|---|---|---|---|---|---|---|
| I.1 | Reconcile the estate against the ownership record | What is done about a serial in one and not the other | Pull both lists and diff them | The management server's API on one side; the ownership record's API where the vendor exposes one, its export where it does not | An empty diff, or a diff where every serial has a named owner and a next action | | | 🧭 | |
| I.2 | Find out how devices enrolled, on a sample | The sample size, and what *supervised, non-removable* has to be true of | Run the read-only check on each sampled machine and classify the results | `profiles status -type enrollment` via the management server's script channel or SSH | Every sampled machine classified, and every classification traceable to its command output | | | 🧭 | |
| I.3 | Take a key out of escrow and unlock a machine with it | Everything — which machine, and whether the result is trusted | Only the list of machines whose record claims an escrowed key | The management server's API | The person unlocked the machine, today, on the escrow the estate actually uses | | | ⛔ — the row exists to be **witnessed**; an unlock a model reports is the untested escrow the row is there to catch | |
| I.4 | Compare installed profiles against what the console says it sent | What counts as drift worth acting on | Read both sides and diff them, per machine in the sample | `sudo profiles list` on the machine; the profile set from the management server's API | A byte-for-byte match per profile, or a listed difference — **not** a console count | | | 🧭 | |

---

*Rows are added when a runbook hop or a docs/03 row is handed to a model for the first time,
never ahead of that. The next rows to earn a model line are in [TODO.md](TODO.md).*
