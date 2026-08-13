# Step 3 — BPA (Best Practice Analyzer for AI-readiness)

**Goal:** measure the model against explicit AI-readiness rules before you start fixing.

Run these as **Tabular Editor** Best Practice Analyzer rules, or hand the rule list to the agent
and ask it to check the connected model via the Power BI Modeling MCP. The machine-readable rules
are in [`rules.json`](rules.json).

## Prompt

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Evaluate the connected model against the AI-readiness rules in rules.json (attached).
For each rule, list every violating object with its name. Then give:
- a per-rule pass/fail count,
- the top 10 highest-impact fixes for Copilot readiness,
- nothing applied yet.

Present as a table grouped by severity (error / warning / info). Wait for my approval before
proposing fixes in later steps.
```

## You review
- The violation list and severity — this becomes your fix backlog for steps 4–5.
