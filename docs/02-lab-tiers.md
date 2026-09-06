# Lab tiers

Three environment levels. What matters about each is not what it can build — it is the hop
it **cannot** verify, stated up front.

🚧 *Boundaries settled. Build instructions fill in per tier.*

| Tier | What it is | Verifies through | **Stops at** |
|---|---|---|---|
| **Minimum** | One machine, no additional hardware | Profile authoring and inspection · packaging automation end to end · client-pull distribution including an unattended in-place upgrade · a local certificate authority issuing an identity, and a profile that references it correctly | No management server, so **no delivery** and no ownership-record handoff · no authenticator and no authentication server, so **no association** — a credential can be shown to exist and be correctly referenced, never to be accepted |
| **Mid** | + a RADIUS server and 802.1X-capable hardware, on an isolated segment | The full EAP-TLS association · trust-anchor pinning actually rejecting a wrong issuer · the unbound-identity prompt · an expired certificate reproducing the deadlock | Everything is issued and installed **by hand**. Nothing here proves the automation: enrolment at scale, renewal before expiry, or an unreachable enrolment endpoint |
| **Full** | + a management server with an enrolment connector, an organisational ownership record, and a real issuing CA | The whole chain from power on, with nobody present | Nothing in the chain. The limit becomes cost, a multi-week organisational verification, and the burden of running a CA whose failure takes the estate off the network |

## Where this design currently sits

**Minimum.** Hops 5 and 6 are ⛔ **Specced-Not-Run**, and the reason is specific rather than
general: standing up 802.1X honestly requires a certificate authority, an authentication
server, and a handshake against real network hardware. On a single machine that is also the
working machine, the failure mode is **losing the network**, not losing an afternoon.

That is a cost decision, and stating it is the point. A tier list whose limits are unstated
is a runbook. A tier list that names them answers the only question worth asking about
someone else's lab: *what does this actually prove?*
