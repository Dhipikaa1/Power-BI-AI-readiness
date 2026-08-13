# Sample Model — ContosoRetailMini

A tiny retail star schema used to demonstrate the pipeline end-to-end. It ships in **two versions**:

| Folder | State | AI-Readiness Score |
|--------|-------|:------------------:|
| [`before/`](before/) | Cryptic names, no descriptions, keys visible, one bi-directional relationship, `Quantity` mistyped, no date table | **12.6 / 100** |
| [`after/`](after/) | Business names, descriptions, synonyms, hidden keys, fixed types, single-direction relationships, marked date table | **98.5 / 100** |

Both are provided as **TMDL definition files** under
`ContosoRetailMini.SemanticModel/definition/` — this is the substance the scorer and the pipeline
read. Each table has a small inline data sample so the model is self-contained.

## Structure

```
ContosoRetailMini.SemanticModel/definition/
├── database.tmdl
├── model.tmdl
├── relationships.tmdl
└── tables/
    ├── (before) fct_sls · dim_cust · dim_prod · dim_dt
    └── (after)  Sales · Customer · Product · Date
```

## Open it in Power BI Desktop (optional)

TMDL is the model definition only. To open/edit it in Desktop, wrap it in a PBIP project:

1. Create a new PBIP project (File → Save As → `.pbip`) or copy an existing PBIP folder.
2. Replace its `*.SemanticModel/definition/` folder with the `before/` or `after/` definition here.
3. Open the `.pbip` in Power BI Desktop.

> Note: `.pbix` / `.pbip` binaries are git-ignored. Never commit enterprise models to a public repo.

## Score it

```bash
python ../../scoring/ai_readiness_score.py before/ContosoRetailMini.SemanticModel
python ../../scoring/ai_readiness_score.py after/ContosoRetailMini.SemanticModel
```
