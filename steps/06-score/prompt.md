# Step 6 — Score

**Goal:** measure AI-readiness with a reproducible 0–100 score, before and after.

There are two scorers in this repo — use whichever fits where your model lives:

| Scorer | Runs where | Reads the model via | Best for |
|--------|-----------|---------------------|----------|
| **`scoring/AI_Readiness_Score.ipynb`** | Fabric notebook | `semantic-link` (sempy) — **live model** | Published models in a Fabric workspace |
| `scoring/ai_readiness_score.py` | Local Python (stdlib) | TMDL files on disk | PBIP projects / offline / CI |

---

## Primary: live scorer — `AI_Readiness_Score.ipynb` (sempy)

This is the scorer used to produce the numbers in this repo. It connects to a **live semantic
model** with `sempy.fabric` and scores **7 categories, each 0–100, then takes a simple average**:

| # | Category | What it checks |
|---|----------|----------------|
| 1 | Description Coverage | % of tables + columns + measures with non-empty descriptions |
| 2 | Naming Quality | % of business-friendly names (no `vw_`, `tbl_`, GUIDs, ALL_CAPS) |
| 3 | Relationship Health | Penalty for BiDi (−15), M:M (−20), M:M+BiDi (−30) |
| 4 | DAX Quality | Anti-patterns + complexity + format strings + calc-column ratio |
| 5 | Column Metadata | Data-type coverage (60%) + ID/key columns hidden (40%) |
| 6 | Model Structure | % of tables classifiable as Fact / Dim / Bridge / Parameter / Utility |
| 7 | Relationship Coverage | Relationship-to-table ratio + inactive-relationship check |

**Grade:** A (90+) · B (80+) · C (70+) · D (60+) · F (<60)

### Run it
1. Upload [`../../scoring/AI_Readiness_Score.ipynb`](../../scoring/AI_Readiness_Score.ipynb) to a Fabric workspace.
2. In the **PARAMETERS** cell set `WORKSPACE_NAME`, `DATASET_NAME`, and (optionally) `ALERT_THRESHOLD`.
3. Run all cells — it prints a per-category breakdown, a visual scorecard, and an alert if the
   score falls below the threshold.
4. Schedule it via a Fabric Pipeline for recurring, alerting AI-readiness checks.

> Requires `semantic-link` (pre-installed in Fabric).

---

## Alternative: offline scorer — `ai_readiness_score.py`

Dependency-free (stdlib only). Parses a model's **TMDL** on disk and scores it against weighted
rules — handy for PBIP projects, local runs, and CI where there's no live Fabric connection.

```bash
# From the repo root
python scoring/ai_readiness_score.py sample-model/before/ContosoRetailMini.SemanticModel --out results/before.json
python scoring/ai_readiness_score.py sample-model/after/ContosoRetailMini.SemanticModel  --out results/after.json
```

On the bundled sample model this produces **12.6 → 98.5** (the 6 steps were run live through the
Power BI Modeling MCP). See [`../../docs/before-after.md`](../../docs/before-after.md) for the breakdown.

---

## Prompt (optional — score any live model through the agent)

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Compute the AI-Readiness Score for the connected model. If it lives in a Fabric
workspace, use scoring/AI_Readiness_Score.ipynb (sempy, 7 categories, simple average).
Otherwise export the model's TMDL and use scoring/ai_readiness_score.py. Report the overall
score, the per-category breakdown, and the three lowest categories with concrete fixes.
```

## You review
- The before/after breakdown, and the lowest-scoring categories to iterate on.
