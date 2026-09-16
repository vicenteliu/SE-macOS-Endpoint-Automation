# Lab tiers

Three environment levels. What matters about each is not what it can build — it is the hop
it **cannot** verify, stated up front.


| Tier | What it is | Verifies through | **Stops at** |
|---|---|---|---|
| **Minimum** | One machine, no additional hardware | Profile authoring and inspection · packaging automation end to end · client-pull distribution including an unattended in-place upgrade · a local certificate authority issuing an identity, and a profile that references it correctly | No management server, so **no delivery** and no ownership-record handoff · no authenticator and no authentication server, so **no association** — a credential can be shown to exist and be correctly referenced, never to be accepted |
| **Mid** | + a RADIUS server and 802.1X-capable hardware, on an isolated segment | The full EAP-TLS association · trust-anchor pinning actually rejecting a wrong issuer · the unbound-identity prompt · an expired certificate reproducing the deadlock | Everything is issued and installed **by hand**. Nothing here proves the automation: enrolment at scale, renewal before expiry, or an unreachable enrolment endpoint |
| **Full** | + a management server with an enrolment connector, an organisational ownership record, and a real issuing CA | The whole chain from power on, with nobody present | Nothing in the chain. The limit becomes cost, a multi-week organisational verification, and the burden of running a CA whose failure takes the estate off the network |

## Build

### Minimum — one Mac, no extra hardware (this is the one the repository's runs used)

Everything here is on a single macOS machine; it is what [phase 3](../phases/3-software/) ran on
and what [`lab/verify.sh`](../lab/verify.sh) re-read. Versions are the current **stable** ones, not
the newest tags ([phase 3, hop 3](../phases/3-software/) says why): macOS 26.6.2, Apache 2.4.67
(the built-in server), Munki 7.3.0, AutoPkg 2.9.0.

1. **Serve a repository.** The built-in Apache needs only to be started and pointed at a repo:
   ```sh
   sudo apachectl start
   sudo mkdir -p /Users/Shared/munki_repo/{catalogs,manifests,pkgs,pkgsinfo,icons}
   sudo ln -s /Users/Shared/munki_repo /Library/WebServer/Documents/munki_repo
   ```
   The directory itself must return **403** (indexing off) and a catalog **200** — the phase-3
   check, and `verify.sh`'s.
2. **The client and the packaging automation.** Install the Munki tools and AutoPkg, add a recipe
   source, author an override — the supply-chain gate is the override's pinned trust
   ([phase 3, hop 3](../phases/3-software/)):
   ```sh
   autopkg repo-add recipes
   autopkg make-override <Recipe>.munki
   ```
3. **Profiles need nothing extra.** Authoring and inspection are in the OS — `profiles`,
   `profiles show -output stdout-xml`, `fdesetup`, `diskutil apfs listCryptoUsers` — which is why
   phases 1 and 2's read-only rows run here with no server ([`lab/verify.out`](../lab/verify.out)).
4. **The identity-reference check** (the credential half the minimum tier *can* reach): a local CA
   with `openssl`, an identity, and a `.mobileconfig` whose network payload's certificate reference
   resolves to the identity payload's identifier — authored and inspected before install. It shows
   a credential *exists and is correctly referenced*; it **stops** there, because acceptance needs
   an authenticator (the mid tier). This is the build; the run is phase 4's, which is ⛔.

Teardown is the phase-3 lab's: drop the web-root symlink and the repository, remove the override.

### Mid — add a RADIUS server and 802.1X hardware, on an isolated segment

Not built here. What to add: a RADIUS/authentication server (FreeRADIUS is the upstream), an
802.1X-capable switch or access point, and a segment that is isolated so a wrong handshake costs
nothing. That is what turns phase 4 from ⛔ into 🔨 for the association, the trust-anchor
rejection, the unbound-identity prompt, and the expiry deadlock — and it still installs
everything by hand, so it proves the model, not the automation.

### Full — add a management server, an ownership record, and a real issuing CA

Not built here, and the reason is in the table: on a single working machine, standing up an MDM
with an enrolment connector, an organisational ownership record and a production CA is a cost and
an operational burden whose failure takes the estate off the network. Named, not run.

## Where this design currently sits

**Minimum.** Hops 5 and 6 are ⛔ **Specced-Not-Run**, and the reason is specific rather than
general: standing up 802.1X honestly requires a certificate authority, an authentication
server, and a handshake against real network hardware. On a single machine that is also the
working machine, the failure mode is **losing the network**, not losing an afternoon.

That is a cost decision, and stating it is the point. A tier list whose limits are unstated
is a runbook. A tier list that names them answers the only question worth asking about
someone else's lab: *what does this actually prove?*
