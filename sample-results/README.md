# Sample results

These are the actual audit workbooks produced by running the repo's prompts against the
**before** sample model ([`../sample-model/before`](../sample-model/before)). They show what
each step's **Audit** phase hands you to review before anything is changed.

| File | Produced by | Sheets |
|------|-------------|--------|
| [`01_Cleanup_Dependency_Audit.xlsx`](01_Cleanup_Dependency_Audit.xlsx) | [Step 1 — Cleanup](../steps/01-cleanup/prompt.md) | Object Inventory · Relationships · Dependency Tree · Unused Summary · Optimization |
| [`02_AI_Readiness_Relationship_Analysis.xlsx`](02_AI_Readiness_Relationship_Analysis.xlsx) | [Step 2 — Optimize](../steps/02-optimize/prompt.md) | 10 sheets: Executive Summary → Model Diagram |

## What they found (before model)

- **1 bi-directional relationship** (`fct_cust`) → fix to single direction
- **`dim_dt` not marked as a Date table** → blocks time-intelligence
- **`discourageImplicitMeasures` not set** → Copilot may auto-sum raw columns
- **Visible, summed keys** (`sls_id`, `cust_id`, `prod_id`, `dt_ky`) → hide + summarizeBy None
- **`qty` typed `double`** → should be `int64`
- **1 redundant measure** (`m_tmp_old`) → safe to delete (no dependents)
- No descriptions, cryptic names, no format strings, no synonyms

These findings are exactly what Steps 3–6 then fix, taking the sample from **12.6 → 98.5**.

> Regenerate with `py -3 _build_sample_results.py` from the repo root.
