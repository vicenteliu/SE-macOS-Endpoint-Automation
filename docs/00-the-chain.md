# The chain

Eight hops between a sealed box and a machine someone can work on. Each one is owned by a
different mechanism, and each fails in its own way.

🚧 *Structure settled. Per-hop detail fills in as each is worked through.*

| # | Hop | Owned by | Marker | Phase |
|---|---|---|---|---|
| 1 | Power on → Setup Assistant reaches out | Apple, the device's ownership record | 🔨 | [1](../phases/1-enrolment/) |
| 2 | Ownership record → enrolment profile | ABM/ASM ↔ MDM pairing | 🔨 | [1](../phases/1-enrolment/) |
| 3 | Enrolment → supervision and trust | MDM, bootstrap token | 🔨 partial | [1](../phases/1-enrolment/) |
| 4a | Trust → configuration | Configuration profiles | 🔨 bounded | [2](../phases/2-configuration/) |
| 4b | Configuration → privacy consent | TCC / PPPC | 🧭 | [2](../phases/2-configuration/) |
| 5 | Configuration → credential | SCEP / ACME carried by a profile | ⛔ | [4](../phases/4-network-access/) |
| 6 | Credential → network | 802.1X, EAP-TLS | ⛔ | [4](../phases/4-network-access/) |
| 7 | Network → software | Client-pull distribution + packaging automation | 🔨 lab | [3](../phases/3-software/) |
| 8 | Software → identity | Platform SSO *(optional extension)* | 🧭 | [5](../phases/5-identity-optional/) |

## Why the joints matter more than the links

Every hop above is documented by its vendor. What is not documented is what the next hop
assumes about the previous one — and that is where a zero-touch build actually fails:

- A device that enrols but is not supervised silently loses half the configuration surface.
- A configuration profile that lands before its certificate is a Wi-Fi payload pointing at
  an identity that does not exist yet.
- A machine that cannot authenticate to the network cannot reach the software repository,
  so hop 6 failing looks exactly like hop 7 failing.

**Ordering is therefore part of the design, not an implementation detail.** Each phase
states what must already be true before it runs.

## The constraint that shapes all of it

This design assumes a population that **out-technicals its support organisation** — users
who will notice a control, understand it, and route around it.

That single assumption changes the answer at every hop. "Best practice" becomes a
negotiation rather than an enforcement, adoption becomes load-bearing rather than soft, and
**every phase needs a documented Escape Hatch** — because an undocumented workaround is
worse than a documented exception, and a population like this will find one either way.

A lock-down design is the wrong answer here, and it is the answer most zero-touch writing
assumes.
