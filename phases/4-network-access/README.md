# Phase 4 — Network access

> ⛔ **Specced-Not-Run.** A complete specification, verification steps and acceptance criteria,
> deliberately not executed — with the reason stated per tier rather than waved at once.
> See [ADR-0001](../../docs/adr/0001-specced-not-run-is-a-third-marker.md).

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **How a machine proves who it is** | ⛔ | The three roles, the handshake, and what happens when it fails |
| 2 | **Credential delivery** | ⛔ | Getting a certificate onto a machine nobody has touched |
| 3 | **Tier specification** | ⛔ | What each tier verifies, and the exact hop it stops at |

## Hop 1 — three roles and one question

- **Supplicant** — the machine asking to get on. On macOS this is `eapolclient`.
- **Authenticator** — the switch port or access point. It forwards. **It does not decide.**
- **Authentication server** — RADIUS. It decides.

**EAP** is the envelope; the method inside it is what matters. **EAP-TLS** is mutual certificate
authentication — the client validates the server's certificate *and* presents its own. No shared
secret, no password, which is why enterprises want it and why it is harder to operate.

🔑 **The endpoint half is the half this chain cares about.** The handshake is well documented and
rarely where a deployment fails. What fails is everything upstream of it: how a machine that
nobody has touched ends up holding a private key, and what happens on the day it stops holding a
valid one.

## Hop 2 — credential delivery

One configuration profile carries **both** payloads, and the relationship between them is the part
that gets missed:

- **A certificate payload** obtains the identity — **SCEP**, **ACME**, or a **PKCS #12** file.
  🔑 The first two are the ones that scale, and for a reason worth stating: the device generates
  the key locally and enrols for a certificate, so **the private key is never transported**. A
  PKCS #12 file is a private key in a file, and every copy of that file is a copy of the identity.
- **A network payload** — Wi-Fi or wired 802.1X — that **explicitly references that identity
  payload**.
- **Trust**, in the same payload: the issuing root pinned as the anchor for the authentication
  server, and the server's expected name pinned alongside it.

⛔ **This works because the device is managed.** A private root and an enrolment identity can be
placed on it precisely because it enrolled first ([phase 1](../1-enrolment/)). The same reasoning
run backwards is why an unmanaged device cannot be given a private root — and why services those
devices reach need a publicly-trusted certificate instead. **Same trust boundary, opposite side.**

### How it fails

🥇 **The deadlock is the one worth naming first.** The certificate expires → the machine cannot get
on the network → it cannot reach the management server that would renew the certificate.
**Certificate lifecycle is the actual hard problem here, not the handshake.** It is designed
around, not solved: renew well inside the validity window, keep a path that does not require the
certificate, and decide in advance what an unauthenticated machine gets.

⛔ **And that last decision is not a networking decision.** *What happens to a machine that cannot
authenticate* — quarantine, MAC-address bypass, an exception, a credential issued by hand — is a
question about who is allowed to keep working this morning. It belongs to a person, and pretending
it is a configuration value is how it gets decided by whoever happens to be on shift.

Two more:
- **The network payload does not reference the identity payload.** macOS cannot tell which
  certificate to present and **prompts the person to choose one**. Zero-touch becomes a dialog box
  in front of someone with no basis for answering it.
- **The trust anchor and server name are not pinned.** The supplicant will accept an
  authentication server it should not, which is the entire premise of a look-alike access point.

## Hop 3 — the tier specification

🔴 **The stop point is the payload of this section.** A tier list without one is a shopping list.

### Minimum — one machine, no additional hardware

**Can verify**: a local certificate authority issuing a client identity · a profile carrying that
identity and a network payload that references it · the identity landing in the keychain · the
network payload resolving to that identity rather than prompting.

**Stops at**: no authenticator and no authentication server, so **no association**. Nothing here
proves the credential is accepted — only that it exists and is correctly referenced.

⚠️ **Honest note, because the general reason does not apply here.** This tier touches no network
configuration and carries no risk to a working machine. **It has not been run for a different
reason — it has not been the priority.** Saying so is the difference between a stated reason and
a stated excuse, and this marker is worth nothing if it covers both.

### Mid — a RADIUS server and 802.1X-capable hardware

**Can verify**: the full EAP-TLS association · trust-anchor pinning actually rejecting the wrong
issuer · the unbound-identity failure producing the prompt · an expired certificate producing the
deadlock rather than a clean error.

**Stops at**: everything is issued and installed by hand. Nothing here proves the *automation* —
enrolment at scale, renewal before expiry, or what happens when the enrolment endpoint is
unreachable.

🔴 **This is the tier the risk statement is about.** Standing it up means changing network
configuration on hardware that a working machine depends on; the failure mode is **losing the
network**, not losing an afternoon. That is the stated reason, and it applies here rather than
everywhere.

### Full — management server with an enrolment connector, and a real issuing CA

**Can verify**: the whole chain, including automated enrolment at first boot and renewal without
anyone present.

**Stops at**: nothing in the chain. The limit becomes cost and the operational burden of running
a certificate authority whose failure takes the estate off the network.

## Verification

| Tier | Check | Expect |
|---|---|---|
| Min | Inspect the profile before install | The network payload's certificate reference resolves to the identity payload's identifier — not empty, not a different one |
| Min | After install, inspect the keychain | The client identity present, with its private key, and marked as issued by the pinned root |
| Min | Open the network settings for that profile | The identity selected automatically. **A prompt to choose a certificate is a failure**, not a cosmetic issue |
| Mid | Associate | Authentication succeeds without user interaction |
| Mid | Present a certificate from a different issuer | **Rejected.** If it succeeds, the anchor is not pinned |
| Mid | Set the client certificate's validity to already-expired | The deadlock reproduces — no association, and no path to renewal over that network |
| Full | Erase and enrol a device from nothing | It reaches the network with no human touching it |

## Acceptance

⛔ **Not met at any tier.** The acceptance criterion for this phase is the Mid-tier row above —
**an expired certificate reproducing the deadlock** — because that is the failure the whole design
exists to manage, and a lab that has only ever seen the happy path has not tested the design.

## Escape Hatch

Every phase needs one; this phase **is** one, for the rest of the estate. A machine that cannot
authenticate cannot reach the software repository, the management server, or the identity
provider — so a failure here presents as a failure of everything downstream of it.

- **Name the quarantine path before it is needed**, and make it something a person can be told
  over the phone.
- **Keep one route that does not depend on the certificate.** Wired with MAC-address bypass, a
  guest network with an onboarding page — the specific mechanism matters less than it existing and
  being known.
- ⛔ **Do not make the exception harder to obtain than the workaround.** A population capable of
  configuring its own network profile will configure its own network profile, and then the estate
  has a machine on the network that no policy has ever touched.
