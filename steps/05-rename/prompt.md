# Step 5 — Rename  (Audit → Review → Apply)

**Goal:** business-friendly, consistent names — driven by the **glossary** and the
**descriptions** from Step 4, without breaking meaning.

1. **Propose** — the agent returns a rename map as a CSV. No model changes.
2. **Review** — you approve the `old → new` map.
3. **Apply** — the agent renames and updates **all references** (DAX, sort-by, hierarchies,
   and the PBIP report visuals/filters/slicers).

---

## Phase A — Propose prompt (CSV only, no model changes)

```text
You are a semantic model standardization expert.

Your goal is to improve naming for business readability and consistency.

Use:
1. Semantic model metadata
2. Business glossary
3. The descriptions file from Step 4

Do NOT generate descriptions again. Focus ONLY on renaming.

Propose improved names for:
- Tables
- Columns
- Measures

Rules:
- No abbreviations unless defined in the glossary
- Names must reflect business meaning from the descriptions
- Maintain consistency across the model
- Avoid breaking semantic meaning

Output STRICTLY in CSV format:
Object Type,Table Name,Old Name,New Name,Reason
```

## Phase B — Review (you)
Approve the `old → new` map. This same map is what the agent uses to fix the report,
so keep it exact.

## Phase C — Apply prompt (only after you approve)

```text
Apply the approved renames from the CSV via the Power BI Modeling MCP. CRITICAL: after
renaming, update ALL references so nothing breaks —
- measure & calculated-column DAX,
- sort-by columns and hierarchies,
- the PBIP report (visual bindings, filters, slicers, report-level measures).
Also hide surrogate keys, set SummarizeBy = None on keys/Year/Month/Quarter, and add a
formatString to every measure. Report the old → new map applied and any references fixed.
```
