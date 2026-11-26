# Lab A: context autopsy, failure attribution

Input: `data/novatech/m1/autopsy_transcript.md` (the window NovaBot sent for Priya's question about TCK-1042, and its answer).

One row per failure. Use **one** component per row, chosen from:
`system` · `user_input` · `history` · `knowledge` · `tools` · `memory_state` · `budget` (for cross-cutting problems).
Quote the evidence from the window in "double quotes" (or `backticks` for code and payloads). Describe what is
missing from the **design**, not what the model did wrong. Add as many rows as you find.

Rows are ordered by how much fixing them would change the answer (step 4), most first.

NovaBot's answer, for reference: "Yes — Orbital Foods is a Premium customer, and all Premium and Elite customers receive hotfixes for any supported version, so we can request a hotfix for their NovaSync 2.2 environment." / "Response time: as a Premium customer, Orbital is owed an initial response within 1 hour." / "Next step: I can open a new ticket for the hotfix request if you like." / "Source: Support FAQ."

| # | Component | Evidence (quoted from the window) | What is missing in the design |
|---|---|---|---|
| 1 | system | "Premium customers get 1-hour responses." | Rule that SLA comes only from a cited current source; facts that change must not be hard-coded |
| 2 | memory_state | "(empty)" vs answer "NovaSync 2.2" and ticket "NovaSync 2.3 sync failures after upgrade" | Session state holding customer, ticket, tier and version |
| 3 | knowledge | "All Premium and Elite customers receive hotfixes for any supported version." (DOC-FAQ-003, rank 1, above DOC-POL-001, rank 2) | Source authority metadata and a ranking rule putting policy above FAQ |
| 4 | system | "Never tell a customer no if you can avoid it." | Authority order and conflict rule; if the governing source says no, say no |
| 5 | knowledge | "Do Premium and Elite customers get hotfixes?" (no SLA chunk retrieved) | Retrieval covering every part of the question, and a gap signal |
| 6 | system | "Source: Support FAQ." | Citation format with source ID and clause |
| 7 | tools | "Tool called for this request: ticket_detail" while "Tools defined: 8" and entitlement_check was never called | Tool selection by question (offer and call entitlement_check) and a guard on write tools such as ticket_create |
| 8 | history | "NovaSync 2.3 sync failures since their upgrade from 2.2 on 16 May." (first turn) and "Full ticket dumps inside the history: 3" | A history policy that keeps the customer, ticket and version facts and drops repeated, stale ticket dumps |
| 9 | budget | "Budget 12000: the window is 2.6 times the budget" | Per-component cap, priority and eviction order |
| 10 | tools | "ticket_detail: Return the full record of a single ticket, including every event." | Result cap and trimmed result shape |
| 11 | system | "Sign off as NovaBot." (asker is a staff engineer) | Persona definitions (P1 to P3) and formats; never customer-facing |
| 12 | system | "Old note (2024): NovaSync Home questions go to the consumer team." | Ownership and versioning; only stable rules in system context |
| 13 | user_input | "Is Orbital entitled to a hotfix for this, and what response time do we owe them?" | Step to resolve "this" and "them" to ticket, tier and severity |

## Token table check (step 1)

- Largest component and its share of the window: history, 23,827 of 31,687 tokens, 75.2%. Tool results are next at 7,457 (23.5%). System, knowledge, tool definitions and user input together are 403 tokens (1.3%): the window is almost all payload, with only 133 tokens of the knowledge that matters.
- Is there a budget at all? No. Nothing is capped and nothing was evicted. Under the course's 12,000-token window with a 1,500-token response reserve, 10,500 tokens are available. The starter spec allocates history 2,500, tool results 1,500, knowledge 3,500, system 800, so history would be about 10% of what NovaBot sent and tool results about 20%.

## Pair compare (step 3)

There was no pair partner in this session, so this is my own resolution of the three places where two components could both take the blame:

- **SLA claim (#1 system vs #5 knowledge).** Quoted evidence settles it: the 1-hour figure appears word for word in the system prompt ("Premium customers get 1-hour responses."), and the retrieved chunks contain no response time at all. The wrong number came from system context. Knowledge's gap (#5) is real but did not produce the claim.
- **Eligibility "Yes" (#3 knowledge vs #4 system).** Both chunks were present, so retrieval had the right policy; the FAQ outranked it. The FAQ's wording "any supported version" is what the answer reproduced. A ranking and metadata change (knowledge) fixes it at source; a conflict rule (system) fixes it for any ranking. I rank knowledge first for this symptom and keep system as the cheaper interim control.
- **Wrong version (#2 memory_state vs #8 history).** History did contain the right version ("NovaSync 2.3" in T01 and in every ticket copy), so history was not missing the fact; it had four copies and no way to say which is current. Design change that fixes it first: state, which holds the version in one place.

## Top three and fix first (step 4)

1. **#1 system, hard-coded SLA.** Changes the whole second bullet of the answer.
2. **#2 memory_state, no version or ticket in state.** Changes the first bullet, and eligibility depends on it.
3. **#3 knowledge, FAQ ranked above policy.** Changes the source and the reasoning of the first bullet.

**Fix first:** finding #1, system. System context is the highest-authority input, so a wrong fact there overrides any correct retrieval, state or tool result: fixing state or ranking first would still leave a confident, uncited "1 hour". It is also the cheapest fix (delete one line and add a grounding rule), and it is a Module 1 change that needs no new infrastructure.
