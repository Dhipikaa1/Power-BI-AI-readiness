# Step 2 — Optimize

**Goal:** a clean star schema with correct types and simple, explicit measures — the foundation
Copilot relies on.

## Prompt

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Review the model for structural quality and propose fixes. Present findings first;
apply only what I approve.

Check and propose fixes for:
1. Data types — every column has the correct dataType; numeric IDs are Whole Number.
2. Relationships — single-direction where possible; flag bi-directional and many-to-many
   with the reason they exist and a safer alternative.
3. Explicit measures — every key metric is an explicit measure (no implicit aggregations).
4. DAX simplification — rewrite over-complex measures to clearer, equivalent DAX.
5. Date table — a marked date table exists for time-intelligence.

Output a table: issue, object, current, proposed, risk. Wait for approval, then apply
approved changes via MCP and confirm.
```

## You review
- Relationship direction changes (can affect existing visuals).
- Any DAX rewrite — confirm results are identical.
