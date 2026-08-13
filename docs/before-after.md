# Before → After — Sample Model Results

These numbers are **measured**, not illustrative. The 6 steps were run **live against the model
through the Power BI Modeling MCP** (the GitHub Copilot agent applying each step's prompt), and the
bundled scorer ([`scoring/ai_readiness_score.py`](../scoring/ai_readiness_score.py)) was run on the
exported TMDL before and after. Reproduce the score yourself:

```bash
python scoring/ai_readiness_score.py sample-model/before/ContosoRetailMini.SemanticModel --out results/before.json
python scoring/ai_readiness_score.py sample-model/after/ContosoRetailMini.SemanticModel  --out results/after.json
```

## AI-Readiness Score

| | Before | After |
|---|---|---|
| **AI-Readiness Score** | **12.6 / 100** | **98.5 / 100** |

## Per-rule breakdown

| Rule | Weight | Before | After |
|------|:------:|:------:|:-----:|
| Measure descriptions | 14 | 0% | 100% |
| Visible-column descriptions | 12 | 0% | 100% |
| Table descriptions | 8 | 0% | 100% |
| Business-friendly names | 14 | 0% | 100% |
| Key/ID columns hidden | 8 | 0% | 100% |
| Keys/Year summarize = None | 5 | 0% | 100% |
| Measures have format strings | 7 | 0% | 100% |
| Synonyms defined | 8 | 0% | 81% |
| Date table marked | 8 | 0% | 100% |
| Single-direction relationships | 8 | 66% | 100% |
| Correct data types | 8 | 90% | 100% |

*(Before isn't 0 — a legacy model usually has some things right, like most data types and
some single-direction relationships. After scores 81% on synonyms because the scorer
conservatively doesn't count table-level synonyms, so the total is a realistic 98.5, not 100.)*

## Live scorer (sempy notebook)

The same model, scored with [`scoring/AI_Readiness_Score.ipynb`](../scoring/AI_Readiness_Score.ipynb)
(7 categories, each 0–100, simple average). This is the scorer that runs against a **live** model
in Fabric; the numbers below were produced by running its exact logic on the before/after TMDL.

| Category | Before | After |
|----------|:------:|:-----:|
| Description Coverage | 0.0 | 75.0 |
| Naming Quality | 82.8 | 100.0 |
| Relationship Health | 85.0 | 100.0 |
| DAX Quality | 70.0 | 100.0 |
| Column Metadata | 60.0 | 100.0 |
| Model Structure | 75.0 | 100.0 |
| Relationship Coverage | 100.0 | 100.0 |
| **Overall** | **67.5 (D)** | **96.4 (A)** |

*Model Structure reaches 100 because the after tables carry explicit role names
(`Fact Sales`, `Dim Customer`, `Dim Product`, `Dim Date`) that the notebook's classifier
recognizes. Description Coverage caps at 75 by design — hidden surrogate keys have no
descriptions but still count in the denominator.*

## What actually changed

| | Before | After |
|---|---|---|
| Table names | `fct_sls`, `dim_cust`, `dim_prod`, `dim_dt` | `Fact Sales`, `Dim Customer`, `Dim Product`, `Dim Date` |
| Measure names | `m_ttl_sls`, `m_avg_disc`, `m_sls_ytd` | `Total Sales`, `Average Discount %`, `Sales YTD` |
| Column names | `txn_amt`, `disc_pct`, `dt_ky`, `cust_id` | `Sales Amount`, `Discount %`, `Date Key` (hidden), `Customer Key` (hidden) |
| Descriptions | none | every visible table, column, measure |
| Synonyms | none | on every visible column & measure |
| Surrogate keys | visible, summed | hidden, `SummarizeBy = None` |
| Format strings | none | `$` on currency, `%` on rates |
| Data types | `Quantity` stored as decimal | corrected to Whole Number |
| Relationships | one **bi-directional** | all single-direction |
| Date table | not marked | marked as date table (time-intelligence) |
| Dead measures | `m_tmp_old` present | removed |

> The model is provided as **TMDL definition files** (the substance the pipeline and scorer read).
> To open it in Power BI Desktop, wrap it in a PBIP project — see [`../sample-model/README.md`](../sample-model/README.md).
