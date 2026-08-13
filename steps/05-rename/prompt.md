# Step 5 — Rename

**Goal:** business-friendly names, hidden keys, and correct format strings.

## Prompt

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Propose a RENAME MAP that makes the model business-friendly, then apply after approval.

For every VISIBLE table, column, and measure:
- Convert technical names to clear business names (fct_sls -> Sales, txn_amt -> Sales Amount,
  m_ttl_sls -> Total Sales, dt_ky -> Date Key).
- Hide surrogate keys / *_id / *_ky columns; set their SummarizeBy to None.
- Set SummarizeBy = None on Year/Month/Quarter and other non-additive numbers.
- Add a formatString to every measure ($ for currency, % for rates, thousands separators).

CRITICAL: when you rename, update ALL references — DAX (measures, calculated columns),
sort-by columns, hierarchies, and the PBIP report (visual bindings, filters, slicers).
Output the rename map (old -> new) and the list of downstream references you will update.
Wait for approval, then apply via MCP and report what changed.
```

## You review
- The **old → new rename map** (this is the mapping the agent uses to fix the report too).
- Confirm the report still renders after renames.
