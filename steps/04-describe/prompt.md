# Step 4 — Describe

**Goal:** give every visible object a concise, AI-useful description and synonyms.

## Prompt

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Draft descriptions and synonyms for every VISIBLE table, column, and measure that is
missing one. Do not invent business meaning — use the DAX, data type, name, and the context
I provide; where a metric is ambiguous, ask me.

Rules for each description:
- 1–2 sentences, plain business English, front-load the key meaning (Copilot reads ~200 chars).
- State units and grain where relevant (USD, %, per order line).
- For measures, note preferred usage and how it differs from similar measures.
- Add 2–5 synonyms per object (the words users actually say: Revenue = Sales = Turnover).

Output a review table: object, proposed description, proposed synonyms. Wait for my approval,
then write the approved descriptions + synonyms to the model via MCP.
```

## You review
- Descriptions for accuracy (this is where business context matters most).
- Synonyms — add any team-specific vocabulary.

## Example (from the sample model)

```tmdl
/// Total gross sales in USD across all transactions. Primary revenue KPI.
measure 'Total Sales' = SUM(Sales[Sales Amount])
    formatString: \$#,##0.00
    annotation Synonyms = Revenue, Total Revenue, Sales
```
