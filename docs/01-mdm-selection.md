# Choosing the management layer

🚧 *Criteria settled. Per-product detail fills in as each is worked through.*

## Disclosure, first

The author maintains [`muster`](https://github.com/vicenteliu/muster), an open-source fleet
agent. **It is not a candidate below.**

Saying so is cheaper than leaving it to be discovered. A vendor-neutral comparison written
by someone shipping a product in the same category stops reading as a framework and starts
reading as a pitch, and a reader cannot un-notice that once they have noticed it. Keeping
`muster` out protects the comparison's neutrality and lets `muster` remain what it is — a
build-to-learn project, not a candidate in its author's own selection framework.

It also does not implement the Apple MDM protocol, so it is not an alternative to anything
here on the merits either.

## The candidates, and what may honestly be said about each

| | Marker | What that means here |
|---|---|---|
| **Jamf Pro** | 🔨 bounded | Operated: console work, policy and profile scoping, and the API driven for both inventory reads and policy writes. Bounded to a regional testing-and-maintenance remit within a larger estate — not tenant ownership |
| **Workspace ONE / UEM** | 🔨 | Operated: a BYOD programme end to end, and application distribution targeted by user, group, region and country |
| **Microsoft Intune** | 🧭 | **Never run.** The API surface and the management model are mapped; nothing here says how to operate it |
| **Kandji** | 🧭 | **Never run.** Present because it changes the answer for some fleet shapes, not because of experience with it |

⛔ **Consequence, stated rather than implied**: for the two marked 🧭 this document says
what they solve and what they cost. It never says how to operate them, and no sentence here
should be readable as operating experience.

## The axis that actually decides it

Not the feature matrix. Three questions, in this order:

1. **What is the licensing unit — the device or the person?** This inverts the cost answer
   depending on how many devices each human carries, and it is the single largest driver at
   any real fleet size. Two organisations of identical headcount land on different products
   for this reason alone.
2. **What else is already in the building?** A management layer that shares an identity
   provider and a compliance surface with what is already deployed is cheaper than its
   licence line suggests. One that does not is more expensive than its licence line
   suggests.
3. **How many administrators, and what is their day actually made of?** Fleet size does not
   set staffing; the ratio between them varies by roughly an order of magnitude across real
   organisations, and the variable is how much of the estate is exception rather than
   standard.

## The layer that is not a route

Client-pull software distribution and packaging automation (see
[phase 3](../phases/3-software/)) sit **underneath** whichever product is chosen. Treating
them as a third option against Jamf or Intune is a category error that shows up in a lot of
comparison writing: they answer a different question, and a specification naming both an
MDM and a packaging toolchain is describing a division of labour, not listing competitors.

## Escape Hatch

*(To be written: what a user does when the sanctioned product blocks legitimate work, and
what the exception costs the organisation.)*
