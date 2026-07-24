# Knowledge system map

This is the “ontology-lite” the agent should load for Tool 2.

```text
control/docs/
  02_domain_rules.md      ← columns, groups, sum rules
  03_short_questions.md   ← phrase → action
  04_scenarios.md         ← fictional S1 story
  05_prompts.md           ← longer paste prompts if needed

.env                      ← spreadsheet id/tab (machine local)
```

## Design idea

| Layer | Role |
|-------|------|
| Rules | What a valid table is |
| Scenarios | What story we fill (fictional) |
| Short questions | How users talk |
| Scripts | Deterministic demo path |

Long workshop prompts shrink over time into **one-line questions** because rules live in MD—not only in the chat history.

## Agent load order

1. Rules  
2. Short questions  
3. Active scenario  
4. Execute API write  
5. Verify + human check reminder  
