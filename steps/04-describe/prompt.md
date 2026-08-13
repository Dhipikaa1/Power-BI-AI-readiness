# Step 4 — Describe  (Audit → Review → Apply)

**Goal:** give every table, column, and measure a concise, business-friendly description —
grounded in a **glossary**, never invented.

1. **Generate** — the agent drafts descriptions as a CSV. No model changes.
2. **Review** — you check them against the business (this is where accuracy matters most).
3. **Apply** — the agent writes the approved descriptions (and synonyms) to the model.

Provide a **business glossary** (abbreviations → meaning). A starter template is in
[../glossary-template.md](../glossary-template.md).

---

## Phase A — Generate prompt (CSV only, no model changes)

```text
You are a Power BI semantic model expert.

Analyze the connected semantic model.

Use the provided glossary strictly to interpret abbreviations and context for
generating descriptions.

Instructions:
1. Understand the business meaning of each table and column
2. Do NOT rename anything
3. Do NOT infer beyond the given context
4. If unclear, give a generic but safe description

Focus on:
- Business meaning
- Relationships context
- Technical logic

Generate business-friendly descriptions for:
- Tables (including calculated)
- Columns (including calculated)
- Measures

Guidelines:
- Expand abbreviations using the glossary
- Keep it concise (Copilot reads ~200 characters — front-load the meaning)

Output STRICTLY in CSV format:
Object Type,Table Name,Column Name,Object Name,Description
```

## Phase B — Review (you)
Check the CSV against the glossary and business reality. Edit any description; this is
the highest-value human checkpoint.

## Phase C — Apply prompt (only after you approve)

```text
Write the approved descriptions from the CSV to the connected model via the Power BI
Modeling MCP (table / column / measure Update → description). Optionally add synonyms
from the glossary. Do NOT rename anything and do NOT change any other property.
Report how many objects were updated.
```
