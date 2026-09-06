# Phase 3 — Software distribution

> Network to installed, updated, and inventoried.

🔨 **The only phase here with a run behind it.** Stood up end to end on one machine, one
afternoon, two applications. ⛔ **No fleet.** The claim that supports is *the pipeline was built
and it is known where it bites* — not operational experience at scale, and not a war story.

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **Repository model** | 🔨 lab | The server is a web server; the client decides |
| 2 | 🥇 **Blocking and version comparison** | 🔨 lab | One metadata array does two jobs — and the second is what happens when the user is inside the application |
| 3 | **Packaging automation** | 🔨 lab | Processor chains, overrides, and trust pinning as a supply-chain control |
| 4 | **Package internals** | 🧭 | Payload vs payload-free, install scripts, signing, notarisation |

## Prerequisites

- A macOS machine that can serve HTTP. The system Apache is enough; a repository directory
  symlinked into the web root is the whole server.
- The client tools and the automation tools installed. ⚠️ Check the **stable** version, not the
  newest tag — see *Hop 3* for why that sentence exists.
- One vendor disk image to import by hand, and one application already installed at an **older**
  version. The second is what makes the acceptance criterion meaningful.

## Hop 1 — the repository model

A repository is five directories — `catalogs/ icons/ manifests/ pkgs/ pkgsinfo/` — served over
plain HTTP. **There is no application on the server side.** The client signs in on a schedule,
reads the manifest it is assigned, resolves the catalog, and decides for itself what is missing.

🔑 **That inversion is the design argument.** A management server that pushes an install issues a
command and finds out later, or never. A client that pulls produces a *state* — installed, needed,
blocked — that is visible on the machine and true regardless of whether the server was reachable
an hour ago.

⚠️ **A 403 on the repository root is expected and is not a fault.** macOS Apache ships with
directory indexing off; the root returns 403 while `catalogs/<name>` returns 200. The client never
lists a directory — it fetches known paths. Anyone debugging by loading the root in a browser
concludes the server is broken and is wrong.

## Hop 2 — 🥇 one array, two jobs

The imported metadata carries an `installs` array: a path that should exist once the item is
installed, with a version key to compare against. Its documented job is **version comparison** —
how the client answers *is this present, and is it current*, without trusting a receipts database.

**It is also where the blocking application comes from.** With no `blocking_applications` key
present at all, the client still refused to replace a running application, because the `installs`
array names the application bundle:

```
Need to install Firefox
Downloading Firefox-155.0.1.dmg ... downloaded at 223003 KB/sec
Checking if Firefox.app is running...
Blocking apps for Firefox are running: ["Firefox.app"]
Skipping install of Firefox because blocking applications are running.
```

🔑 **The order is the point: it downloaded first, then checked, then declined.** That is the whole
reason download and install are separate phases — the payload is staged while the person is still
working, so the install itself is short and lands the moment the application closes.

**How it fails:** it does not. It queues, silently, and nobody is told. The item stays needed, the
payload sits in the cache, and every run repeats those three lines. **Nothing there is an error** —
a compliance report shows the machine as pending, and the difference between pending for an hour
and pending for four months is invisible unless somebody is looking for it.

Two smaller edges: if the `installs` path is wrong the version check can never be satisfied, so the
item is needed on every run forever — a permanent re-download that also reads as normal. And the
version key matters: the marketing version string and the build version are different values, and
vendors do not always move them together.

## Hop 3 — packaging automation, and the supply chain underneath it

Recipes are processor chains. A run is observable end to end:

```
URLDownloader → EndOfCheckPhase → Unarchiver → CodeSignatureVerifier
              → DmgCreator → MunkiPkginfoMerger → MunkiImporter → MakeCatalogs
```

**Overrides are the customisation unit** — you do not fork an upstream recipe, you shadow the
inputs. And trust-pinning on the recipe itself is the part that matters most and gets discussed
least: **this machinery downloads vendor binaries from the internet and installs them on every
machine you own.** The signature check inside the chain is the control; the recipe-trust check is
the control on the control.

⚠️ **Two things found by running it that reading it did not produce:**

**The tooling's own signing is uneven.** The client tools arrived signed and notarised; the
automation tool arrived unsigned. 🥇 The irony is worth carrying: the automation tool's own
signature-verification processor validated a vendor application's signature *during the run*,
while the tool itself had none. Not a defect — it is the project's norm — but on a managed fleet
it is a policy question before it is a technical one.

**A careful documentation pass produced three wrong version facts** (checked 2026-09; specifics
age, the lesson does not): a version that had never shipped was treated as stable, a feature was
attributed to a release that already had it, and two sources were read as contradicting each other
when one date had been misread. **Anyone following those notes would have put a release candidate
into production.** This is the clearest argument in this repository for the marker system: doc-checked
and run are different states, and the gap between them is not small.

## Hop 4 — package internals 🧭

Payload versus payload-free, pre- and post-install scripts, signing, notarisation, stapling.
⛔ **Mapped, not run.** Both applications in the run installed by copying an application bundle out
of a disk image, which exercises none of it — the one adjacent detail observed is that this install
type has the client repair ownership and permissions afterwards.

## Verification

Per hop, the command and the expected output.

| | Command | Expect |
|---|---|---|
| 1 | `curl -so /dev/null -w '%{http_code}' http://localhost/<repo>/` | **403** — indexing off, not a fault |
| 1 | `curl -so /dev/null -w '%{http_code}' http://localhost/<repo>/catalogs/<catalog>` | **200** |
| 2 | Client run **with the application open** | `Blocking apps ... are running` and `Skipping install`, **after** the download line |
| 2 | Client install run with the application closed | `Install of <app>-<newer version>: SUCCESSFUL` in the install log |
| 3 | One automation run over two recipes plus the catalog rebuild | the full processor chain above, and a signature verification inside it |

⚠️ The import command is **not** fully non-interactive even with the non-interactive flag — it
still prompts about creating a product icon. Anything scripting it has to account for that.

## Acceptance

🔴 **A first install is not the acceptance criterion. An unattended upgrade is.**

Installing something on a machine that did not have it proves the transport works. The criterion
that proves the *model* works is an application that was **already installed at an older version**
moving to a newer one because a newer version appeared in the repository — with nobody touching
that machine.

```
Install of Cyberduck-9.5.4: SUCCESSFUL          ← first install: transport works
Install of Mozilla Firefox-155.0.1: SUCCESSFUL  ← already at 155.0: the model works
```

✅ Met. ⛔ On one machine, one afternoon, two applications. No fleet, no scheduled runs, no second
client, no authentication on the repository, no recipe authored from scratch — all of those remain
🧭 and none of them is claimed here.

## Escape Hatch

The population this design assumes will notice a control, understand it, and route around it. So
the question is not how to prevent that; it is **why they would**.

🔑 **If the sanctioned path is slower than downloading from the vendor, the sanctioned path loses**,
and no policy fixes that. The escape hatch is therefore a design constraint on the main path, not
an exception process bolted beside it:

- A **self-service catalog** that is genuinely faster than a browser. This is the whole hatch, and
  it is upstream of everything else.
- A **documented request path** for anything not in the catalog, with a stated turnaround. An
  undocumented workaround is worse than a documented exception, because the first one is invisible.
- **Instrument rather than forbid.** Where local administrator rights exist for a population that
  needs them, the useful posture is knowing what arrived outside the pipeline — not pretending
  nothing did.

⛔ What is deliberately *not* here: an approval workflow that adds days. On this population that
converts a visible exception into an invisible one, which is the outcome the hatch exists to avoid.
