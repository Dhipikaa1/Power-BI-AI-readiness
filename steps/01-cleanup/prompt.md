# Step 1 — Cleanup

**Goal:** remove dead weight so Copilot sees only meaningful objects.

## Prompt

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Analyze the connected model and produce a CLEANUP report. Do NOT delete anything yet.

Find and list, with evidence:
1. Measures never referenced by any other measure, calculated column, or report visual.
2. Columns that are hidden AND not used in any relationship, measure, sort-by, or hierarchy.
3. Tables with no relationships and not referenced by any measure or visual.
4. Duplicate or near-duplicate measures (same DAX intent under different names).

For each item output: object type, fully-qualified name, why it looks unused, and a
risk level (safe / review / keep). Group by risk. End with a short summary count.

Wait for my approval. After I approve, delete ONLY the items I confirm, one batch at a
time, and report what was removed.
```

## You review
- The **deletion list** (especially anything marked *review*).
- Re-run any dependent report after deletions.
