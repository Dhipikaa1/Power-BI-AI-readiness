# Step 6 — Score

**Goal:** measure AI-readiness with a reproducible 0–100 score, before and after.

This repo ships a dependency-free scorer that parses the model's TMDL and scores it against
eight weighted rules (see [`../../scoring/ai_readiness_score.py`](../../scoring/ai_readiness_score.py)).

## Run it

```bash
# From the repo root
python scoring/ai_readiness_score.py sample-model/before/ContosoRetailMini.SemanticModel --out results/before.json
python scoring/ai_readiness_score.py sample-model/after/ContosoRetailMini.SemanticModel  --out results/after.json
```

On the bundled sample model this produces **12.6 → 98.5** (the 6 steps were run live through the
Power BI Modeling MCP). See
[`docs/before-after.md`](../../docs/before-after.md) for the full breakdown.

## Prompt (optional — score any live model)

```text
You are a Power BI semantic-model engineer working through the Power BI Modeling MCP.

Task: Export the connected model's TMDL definition, then compute the AI-Readiness Score using
scoring/ai_readiness_score.py. Report the total and the per-rule breakdown, and list the three
lowest-scoring rules with concrete fixes.
```

## You review
- The before/after breakdown, and the lowest-scoring rules to iterate on.
