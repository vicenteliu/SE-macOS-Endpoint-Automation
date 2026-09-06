# Phase 6 — Operations and communication

> What happens after day one — which is most of the time, and is where the design either holds or
> gets routed around.

| # | Hop | Marker | What it answers |
|---|---|---|---|
| 1 | **Queue and escalation** | 🔨 | Severity as a lived scheme rather than vocabulary; what a support organisation owes a population more technical than itself |
| 2 | **Support tooling** | 🧭 | A boundary line, stated as one |
| 3 | **Explaining it** | 🔨 | ✅ → [EXPLAIN.md](../../EXPLAIN.md) |

## Prerequisites

A chain that runs. Everything below assumes machines are arriving configured — operations for an
estate that is still built by hand is a different and larger problem.

## Hop 1 — the queue, and what severity actually means

### Three types, not more

**Incident · request · task.** An incident is something that is broken. A request is something
someone wants that the process already allows. A task is work that exists because a person or a
machine moved. 🔑 **Most queue taxonomies fail by growing**, and the cost is not the categories —
it is that nobody can answer *what is actually breaking* once "breaking" is spread across nine
labels.

### Severity, and the number that gives it away

The scheme is four levels, and it only works if two things are true:

- 🔑 **P2 is the resting state of an incident.** If most incidents open at P1, the scheme has
  stopped carrying information and the queue is sorted by whoever writes the most urgent-sounding
  summary.
- 🔴 **P0 is a blast-radius event, and it happens a handful of times a year at most.** Not a busy
  week — a handful a year. **If P0 is being declared monthly, it is not a severity level, it is a
  synonym for "important to me."**

That second number is the whole diagnostic. Ask an operations team how many P0s they had last year
and the answer tells you whether their severity scheme is real, faster than reading their runbooks.

### Tiering, when the users out-technicalise the support team

This is the constraint this chain is designed under
([the chain](../../docs/00-the-chain.md#the-constraint-that-shapes-all-of-it)), and it inverts the
usual advice.

The standard model — tier 1 filters, tier 2 fixes, tier 3 engineers — assumes the person filing
the ticket knows less than the person receiving it. **When that is false, tier 1 is not a filter.
It is a delay**, and a capable person learns within two tickets to route around it.

What survives that inversion:

- **Tier 1 owns what is safe to do unsupervised**, and the boundary is drawn by *what it costs if
  it is wrong on this particular machine*, not by difficulty. A password reset is safe everywhere.
  Reimaging is not, and "reimage it" is exactly the advice a fast tier 1 gives.
- **The escalation path is short and named.** A capable person will accept one hop. They will not
  accept three, and after the second experience of three they stop filing.
- 🥇 **The queue's real job is not throughput, it is memory.** One-off fixes do not accumulate into
  anything; the same fault appearing eleven times is a finding. A queue that cannot answer *what
  recurs* is a logging system with a ticket number.

### The ownership arc, and why it ends

One person absorbing every incident, request and task for a site is fast, coherent, and does not
scale — and the point at which it stops working is not a headcount, it is the first week where
triage displaces the engineering that would remove the tickets. **The exit is splitting the queue
by domain and moving off first-line volume**, and it is a decision that has to be made *before* it
is obviously necessary, because after that point there is no time left to make it.

## Hop 2 — support tooling 🧭

Remote assistance, conferencing, the endpoint side of collaboration platforms. What the category
has to do is stable: reach a machine that may not be on your network, prove who is on both ends,
leave a record, and not become a second unmanaged agent on every device.

⛔ **This document does not speak from operating a named product here**, and says so rather than
listing vendors it has read about. The selection criteria above are the useful half; a product
comparison written from documentation would be a summary of other people's pages.

## Hop 3 — explaining it 🔨

✅ [EXPLAIN.md](../../EXPLAIN.md) — the same chain, zero jargon, with a stated test for whether it
worked. That test is the acceptance criterion for this hop, and ⛔ it has not yet been put to a
real reader.

## Verification

| | Check | Expect |
|---|---|---|
| 1 | Count P0s over the last twelve months | A handful. **A monthly P0 means the scheme is decorative** |
| 1 | Sample open incidents and read their severity | Most sitting at P2. A queue that is mostly P1 is unsorted |
| 1 | Ask the queue *what recurred more than five times this quarter* | An answer, from the data. If it takes a person remembering, the queue is not memory |
| 1 | Trace the last five escalations | One hop each. Three hops means the path is theoretical |
| 3 | Give `EXPLAIN.md` to someone outside the domain | They can name a trade-off they would decide differently. *"That was clear"* is a failure |

## Acceptance

🔴 **The acceptance criterion for an operations phase is not a healthy queue. It is a queue that
got smaller for a reason somebody can name.**

> A recurring fault was identified from the queue's own data, engineered out, and its ticket volume
> went to zero and stayed there.

That is the only outcome that distinguishes operations from ticket-processing, and it is the one
that the throughput metrics everyone reports will never show — closing tickets faster and not
having them are indistinguishable on a dashboard.

## Escape Hatch

🥇 **The escape hatch here already exists, and it is not in the design: it is the back channel.**

A capable person who finds the queue slow will message an engineer they know directly, and it will
work, because the engineer would rather fix it than argue. That is not a discipline failure — it is
the system finding its shortest path.

The design question is not how to close it. It is **whether it produces a record**:

- **Let the back channel exist and make it cheap to log afterwards.** A fix that happened and was
  written down in one line is worth more than a fix that was refused until a ticket appeared.
- ⛔ **Do not make the front door slower than the back one and then police the back one.** That
  converts a visible shortcut into an invisible one, and the queue's memory — the only durable
  thing it produces — quietly stops being true.
- **Watch the ratio, not the incidents.** Back-channel volume rising is a measurement of the front
  door, and it is the earliest signal available that the process has stopped being the fast path.
