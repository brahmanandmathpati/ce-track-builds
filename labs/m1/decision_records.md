# M1 decision records

Three to six lines each. Judgment, not volume. Point at your run reports (`labs/m1/runs/`) for the evidence.

## D-M1-01 Budgets, priorities, assembly order

- **Options considered:** (a) keep the starter budgets; (b) change only history (raise `recent_turns`); (c) re-cut system, history, knowledge and memory from the autopsy and measurements, keep results capped, and reorder the window.
- **Choice:** (c). System 800 to 1,200, history 2,500 to 1,500 with `recent_turns` 6 to 24, knowledge 3,500 to 4,000 (`top_k` 6), memory 1,000 to 800, tool results held at 1,500; 10,100 of 10,500 allocated. Order: system, tool_definitions, state, memory, history, knowledge, tool_results, user_input (stable first, evidence next to the question). Evict history, tool_results, knowledge, memory, tool_definitions, state.
- **Evidence from the runs (tokens, history kept / excluded, violations):** `example_spec_20261126-161126.md`: history 5 kept / 17 excluded, 149 of 2,500 tokens used, T01 (the only turn naming Orbital, CUST-0001, TCK-1042) dropped by the 6-turn window, and a `system` violation (1,075 tokens against 800). `spec_v1_20261126-161124.md`: 19 kept / 3 excluded, 1,371 of 1,500 tokens, no violations; the 3 excluded turns are the 6,953-token ticket dumps. Fake-client runs, so these figures are model-independent but answer quality is not yet scored.
- **Risk accepted:** `recent_turns: 24` fits this 22-turn session; a longer one will cut the oldest turns, so the customer, ticket and version must live in state (fields listed in the spec). Priorities and evict order are commitments until M4 to M7 enforce them. The assembly order is untested on the real model. 400 tokens are left unallocated on purpose.

## D-M1-02 Source-authority and conflict rule

- **Options considered:** (a) trust the highest-ranked retrieved chunk; (b) newest document wins; (c) a fixed authority order, where a document that declares itself authoritative wins, and the conflict is always shown with both citations.
- **Choice (the authority order, and how a conflict is shown to the user):** (c). Order: authoritative policy, other current policy, advisories and guides (workarounds only), FAQs, then history and memory; customer facts: live record, state, history. A conflict is shown as the governing answer first, then "Conflict:" with both citations, then "Governing:" with the reason, then a request to reconcile the documents. If no rule decides it, both are stated and no yes or no is given. See `context_spec/system/v1/conflicts.md`.
- **Why:** The autopsy answered "Yes" from an FAQ ranked above the policy (Lab A #3, #4), and "Never tell a customer no" rewarded agreeing. Rank and recency are not authority: DOC-POL-007 §1.2 states it is authoritative for hotfix eligibility, so it must beat DOC-POL-001 §4.2 whatever order retrieval returns them in.
- **Evidence from probe P-2:** Not yet available: the only runs so far use the offline fake client, whose answers are placeholders. The fake runs do confirm the two policy clauses reach the window (248 user-input tokens, within the 500 budget). The criterion to score on the real model: a Premium customer on the previous minor version is not eligible under DOC-POL-007 §3.1, the answer names DOC-POL-007 as governing, and it shows the conflict with DOC-POL-001 §4.2 and both citations.
