# Step 1 — Cleanup  (Audit → Review → Apply)

**Goal:** remove dead weight so Copilot sees only meaningful objects — **without breaking anything.**

This step is the clearest example of the repo's golden pattern:

1. **Audit** — the agent analyzes and produces a report. **Zero changes.**
2. **Review** — you read the report and pick what's safe to remove.
3. **Apply** — the agent deletes only what you approved.

---

## Phase A — Audit prompt (analysis only, no deletions)

```text
POWER BI SEMANTIC MODEL CLEANUP AUDIT — ZERO-BREAKAGE PROMPT
================================================================================

Objective: Analyze the Power BI semantic model and associated PBIP project to
identify unused, redundant, and dependent objects. Generate an Excel audit report ONLY.

⚠️ DO NOT DELETE ANYTHING. Output is ANALYSIS ONLY.
⚠️ After I review the Excel, I will tell you which specific items to delete.

================================================================================
SCOPE
================================================================================
1. PBIP Report folder path:  <INSERT_PBIP_FOLDER_PATH>
2. Semantic model:  Model '<INSERT_MODEL_NAME>'  Workspace '<INSERT_WORKSPACE_NAME>'
   (connect via the Power BI Modeling MCP)

================================================================================
MANDATORY DATA SOURCES TO QUERY (ALL 8 — DO NOT SKIP ANY)
================================================================================
Query and parse ALL of these before classifying ANY object:
  1. PBIP Report JSON (visuals, filters, slicers, bookmarks, conditional formatting)
  2. Report-level measures (reportExtensions.json)
  3. Model measure DAX expressions (measure Get)
  4. ★ Calculated-table partition expressions (partition Get)
  5. Calculated-column expressions (column Get)
  6. ★ Sort-by-column relationships (column Get → sortByColumn)
  7. Relationship key columns (relationship List)
  8. RLS roles, Perspectives, Calculation Groups

================================================================================
STEP 1: PARSE PBIP REPORT DEFINITION
================================================================================
Walk every visual.json, page.json, report.json and bookmark, and extract:
  1.1 Visual fields — query projections (columns, measures, hierarchies), and
      visual / page / report level filters.
  1.2 Conditional formatting — Conditional.Cases, selector.metadata (Table.Column),
      background/font color, data bars, icons, web URL.
  1.3 Report-level measures (reportExtensions.json) — parse their DAX for column /
      measure references; any model object referenced = NEEDED.
  1.4 Field parameters (CRITICAL) — the parameter table AND every projection it
      controls; mark all as "Used via Field Parameter".
  1.5 Sort definitions — sortDefinition.sort[].field references.
  1.6 Synced slicers — all fields in a syncGroup are globally USED.
  1.7 Bookmarks — fields in bookmark-targeted visuals must be retained.
  1.8 Drillthrough / tooltips — drillFilterOtherVisuals + tooltip page fields.

================================================================================
STEP 2: PARSE THE LIVE SEMANTIC MODEL (via MCP)
================================================================================
  2.1 Tables/columns/measures — column List (incl. hidden); measure List + Get.
  2.2 ★ Calculated tables — partition List (sourceType=Calculated) + Get the DAX;
      ALL columns inside a calculated table are structural → Needed=Yes.
  2.3 ★ Sort-by-column — column Get → sortByColumn / groupByColumns; the target
      column is NEEDED. Check parameter tables, date dimension, category-axis columns.
  2.4 Relationships — both fromColumn and toColumn are NEEDED.
  2.5 Calculated columns — isCalculated flag; Get expressions for upstream deps.
  2.6 RLS roles, Perspectives, Calculation Groups — mark referenced objects NEEDED.

================================================================================
STEP 3: BUILD THE DEPENDENCY GRAPH
================================================================================
For every measure (model + report): parse DAX for 'Table'[Column], Table[Column],
[Measure], and USERELATIONSHIP/CROSSFILTER/TREATAS references.
For every calculated table/column: parse for column references.
Build upstream (depends-on) and downstream (used-by) maps and propagate indirect
usage: if a used object depends on B, and B references column X, then B and X are NEEDED.

================================================================================
STEP 4: CLASSIFICATION
================================================================================
Needed = YES if used in ANY of: a visual projection, a filter, conditional
formatting, drillthrough, tooltip, field parameter, synced slicer, bookmark-targeted
visual, sort definition, model/report measure DAX (direct or indirect), calculated
table/column DAX, as a sort-by target, as a relationship key, inside a calculated
table or field-parameter table, in an RLS role or calculation group, or as a system
table (LocalDateTable/DateTableTemplate).

Safe to Delete = "Yes" only if Needed=No AND Confidence=High.
WHEN IN DOUBT → "Review Required", never "Safe to Delete".

================================================================================
STEP 5: OUTPUT — EXCEL ONLY, NO DELETIONS
================================================================================
Sheet 1 Object Inventory: Table, Object, Type, Source, Needed, Safe to Delete,
  Confidence, Usage Type, Where Used, Dependent On, Used By, Is Key, Is Hidden,
  Is Calc-Table Column, In Perspective, In Role, Sort By Column, Recommendation.
Sheet 2 Relationships: From, To, Cardinality, Cross-filter, Active, Used in Report,
  Used via DAX, Recommendation.
Sheet 3 Dependency Tree: Object, Table, Source, Depends On (measures/columns), Used By.
Sheet 4 Unused Summary: Type, Total, Needed, Not Needed, Safe to Delete, Action.
Sheet 5 Optimization: redundant columns, duplicate measures, BiDi/M:M reviews,
  auto date/time cleanup, report measures to promote to the model.

================================================================================
SAFETY RULES (NON-NEGOTIABLE)
================================================================================
1. Never mark a column unused without checking ALL 8 sources.
2. Never delete columns in calculated tables (structural).
3. Never delete sort-by-column targets or relationship key columns.
4. Never use cached/stale data — always query the live model.
5. Prioritize safety over cleanup — a false "Keep" is fine; a false "Delete" is not.
6. DO NOT modify the model. Wait for my explicit approval before any change.
```

## Phase B — Review (you)
Open the Excel. Confirm the **Safe to Delete (High confidence)** items; move anything
uncertain to keep. You hand back the approved list.

## Phase C — Apply prompt (only after you approve)

```text
Delete ONLY the objects I confirmed below, via the Power BI Modeling MCP, one batch at
a time (measures → columns → tables). After each batch, re-validate that no measure,
calculated table, relationship, or report visual broke, and report what was removed.
Do not touch anything not on my list.

Approved deletions:
<PASTE THE APPROVED ITEMS FROM THE EXCEL>
```
