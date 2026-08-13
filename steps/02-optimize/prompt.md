# Step 2 — Optimize: Relationships & Structure  (Audit → Review → Apply)

**Goal:** a clean star schema — no many-to-many, no unjustified bi-directional filters,
correct types, explicit measures — the foundation Copilot relies on.

1. **Audit** — the agent analyzes relationships & structure and produces a **10-sheet Excel**
   with every issue, all fix approaches, report impact, and a prioritized action plan. **No changes.**
2. **Review** — you pick the fixes from the "Fix Suggestions" sheet.
3. **Apply** — the agent applies the approved fixes and repairs the report.

---

## Phase A — Audit prompt (analysis only, no changes)

```text
AI READINESS — RELATIONSHIP ANALYSIS PROMPT
================================================================================
PURPOSE: Analyze a Power BI semantic model's relationships for AI readiness.
         Produce a multi-sheet Excel workbook with issues, all fix approaches,
         report impact, and a prioritized action plan.
         DO NOT MODIFY ANYTHING — ANALYSIS ONLY.
================================================================================

You are an expert Power BI architect specializing in AI-readiness optimization.
Analyze the semantic model and its associated PBIP report to produce a comprehensive
relationship analysis Excel workbook.

⚠️ DO NOT MODIFY ANYTHING — THIS SESSION IS ANALYSIS ONLY.

INPUTS
  1. Semantic Model: Model '<YOUR_MODEL_NAME>'  Workspace '<YOUR_WORKSPACE_NAME>'
  2. PBIP Report Folder (if available): <YOUR_PBIP_REPORT_FOLDER_PATH>
     (If no PBIP folder, skip report impact analysis and note it in the Excel.)

PHASE 1: CONNECT & INVENTORY (MCP tools) — run ALL, skip none
  1.1  Connect to the model (connection_operations ConnectFabric).
  1.2  List ALL relationships (name, from/to table+column, from/to cardinality,
       crossFilteringBehavior, isActive).
  1.3  List ALL tables and classify each: Fact, Fact(Aggregate), Dimension, Bridge,
       Field Parameter, Measures-Only, Utility, Reference/Mapping, Date Dimension,
       Disconnected, Auto-generated (LocalDateTable_*).
  1.4  Model properties (discourageImplicitMeasures must be TRUE — prevents Copilot
       auto-aggregation; isMdxAvailable — review/set for Excel pivot/MDX behavior;
       discourageReportMeasures; culture; defaultMode).
  1.5  All measures + DAX; flag USERELATIONSHIP / CROSSFILTER / TREATAS; note owning table.
       DAX hygiene: flag `/` division (should be DIVIDE() for divide-by-zero safety) and
       FILTER() that could be KEEPFILTERS() where safe.
  1.6  Security roles (RLS) + table filter expressions; flag relationships used in RLS.
  1.7  Calculation groups + items.
  1.8  Columns for M:M / bridge / BiDi tables (name, dataType, isHidden, sortByColumn).
  1.9  Field-parameter tables (partition DAX → confirm NAMEOF pattern).
  1.10 Report-level measures (reportExtensions.json) — INVISIBLE to Copilot; must migrate.
  1.11 Parse PBIP visuals (pages.json, page.json, visual.json) — types, fields, filters, measures.

PHASE 2: CLASSIFY EVERY RELATIONSHIP
  KEEP · KEEP-AUTO · KEEP-INACTIVE · FIX-MM · FIX-BIDI · FIX-MM-BIDI · FIX-BIDI-PARAM · REMOVE

PHASE 3: GENERATE EXCEL (openpyxl) — EXACTLY these 10 sheets, professional formatting
  (headers #2F5496 white bold; FAIL red #FFC7CE; WARN yellow #FFEB9C; PASS green #C6EFCE):
  1  Executive Summary — totals, issues found, RISK LEVEL (LOW/MEDIUM/HIGH).
  2  Model Inventory — Table | Type | Columns | Measures | Relationships | Notes.
  3  All Relationships — from/to, cardinality, direction, active, category, issue (row-colored).
  4  AI Readiness Issues — why M:M/BiDi break Copilot; issue inventory with severity.
  5  Fix Suggestions (MOST IMPORTANT) — for EVERY issue give 3–4+ approaches
     (fix keys / denormalize / TREATAS / CROSSFILTER / deactivate+USERELATIONSHIP / documented
     exception), each with model+DAX changes, report impact, pros/cons, and one marked
     "YES — BEST".
  6  Report-Level Measures — "INVISIBLE to Copilot"; DAX, tables referenced, migration priority.
  7  AI-Readiness Checklist — M:M=0, BiDi=0, hub tables, uniqueness, blank keys, description %,
     naming, hidden IDs, format strings, discourageImplicitMeasures=TRUE, isMdxAvailable
     reviewed, no auto-date tables (LocalDateTable_*), sort-by-column set on month/day names,
     synonyms defined, DAX uses DIVIDE() (no bare `/`), DAX uses KEEPFILTERS() over FILTER()
     where safe, inactive rels, circular paths (FAIL/WARN/PASS colored).
  8  Report Impact — per page: change applied, impact level, visuals affected, needs recreation?
  9  Action Plan — P0/P1/P2/P3 in dependency order; risk; status = Not Started.
  10 Model Diagram — ASCII star schema, M:M/BiDi areas, recommendations (Consolas).

EXECUTION
  Connect → run ALL Phase-1 inventory → classify (Phase 2) → build the Python/openpyxl
  script with ALL 10 sheets → run it → save to
  output_session1/AI_Readiness_Relationship_Analysis.xlsx → present a summary.

SAFETY: Do NOT modify the model or report. Analysis only. The Excel is reviewed and used
as the input for the Apply phase.
```

## Phase B — Review (you)
Work the **Fix Suggestions** and **Action Plan** sheets: choose one approach per issue
(prefer "YES — BEST"), and confirm which report changes you accept.

## Phase C — Apply prompt (only after you approve)

```text
Apply ONLY the relationship fixes I approved (per the Fix Suggestions sheet), via the Power
BI Modeling MCP: set crossFilteringBehavior to OneDirection, resolve M:M with the chosen
approach, deactivate/activate relationships as decided, set discourageImplicitMeasures=TRUE,
review isMdxAvailable, remove auto-date tables in favor of a proper date dimension, apply DAX
hygiene (DIVIDE() over `/`, KEEPFILTERS() over FILTER()) where safe, set sort-by-column on
month/day name columns, and migrate any report-level measures into the model. After each
change, re-validate the model and the affected report pages, and report exactly what changed.
```
