# Lab tiers

Three environment levels. What matters about each is not what it can build — it is the hop
it **cannot** verify, stated up front.

🚧 *Boundaries settled. Build instructions fill in per tier.*

| Tier | What it is | Verifies through | **Stops at** |
|---|---|---|---|
| **Minimum** | One Mac, local virtualisation | Profile authoring and inspection · packaging automation end to end · client-pull distribution including an unattended in-place upgrade | No MDM push · no ownership-record handoff · no certificate delivery · no 802.1X |
| **Mid** | + an isolated network segment, a managed switch or AP, a local certificate authority | Certificate issuance · profile-carried credential delivery · the shape of an authentication failure | **No EAP-TLS association without the network hardware** — and a machine that cannot authenticate cannot reach the software repository, so this tier cannot distinguish hop 6 failing from hop 7 failing |
| **Full** | + an organisational device-ownership record and an MDM with an enrolment token | The whole chain, from power on | Cost, and a multi-week organisational verification that cannot be shortened |

## Where this design currently sits

**Minimum.** Hops 5 and 6 are ⛔ **Specced-Not-Run**, and the reason is specific rather than
general: standing up 802.1X honestly requires a certificate authority, an authentication
server, and a handshake against real network hardware. On a single machine that is also the
working machine, the failure mode is **losing the network**, not losing an afternoon.

That is a cost decision, and stating it is the point. A tier list whose limits are unstated
is a runbook. A tier list that names them answers the only question worth asking about
someone else's lab: *what does this actually prove?*
