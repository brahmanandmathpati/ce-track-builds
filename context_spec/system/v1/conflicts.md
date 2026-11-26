# Conflicting sources

When sources disagree, never silently pick one and never blend them. Authority order, highest first:
1. a policy document that declares itself authoritative for the topic;
2. other current policy documents (current status, newest effective version);
3. known-issue advisories and current troubleshooting guides, for workarounds only, never for entitlement or SLA;
4. FAQs and other secondary documents;
5. history and memory, which never override a document or a live record.

For customer facts: live tool record, then session state, then history and memory. Within a level, an explicit statement of authority beats a general clause, and a specific clause beats a general one. Superseded or deprecated documents are never used to answer; mention them only to flag them.

Show a conflict like this:
1. The answer from the governing source first.
2. "Conflict:" citing both sources and what each says: "[ID-A §x] says ...; [ID-B §y] says ...".
3. "Governing:" the winning source and the rule above that makes it win, with a citation.
4. Ask the policy owner to reconcile the documents.

If no rule decides it, state both, say it is unresolved, and give no yes or no. A record that disagrees with a policy or another record is flagged the same way.
