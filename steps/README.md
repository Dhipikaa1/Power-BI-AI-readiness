# The 6 Steps

Each step is **prompt-driven** and follows one non-negotiable pattern:

> ## Audit → Review → Apply
> 1. **Audit** — the agent *analyzes only* and produces a report / proposal. **It changes nothing.**
> 2. **Review** — *you* read it and approve exactly what should happen.
> 3. **Apply** — the agent executes *only what you approved*, via the Power BI Modeling MCP,
>    then re-validates that nothing broke.

You run each prompt with **GitHub Copilot (agent mode)** against your model through the
**Power BI Modeling MCP** (or paste it into your LLM of choice). The agent proposes; you approve;
the agent applies. Nothing is written to the model or report without your sign-off.

| # | Step | Audit (agent proposes) | You review |
|---|------|------------------------|-----------|
| 1 | [Cleanup](01-cleanup/prompt.md) | Excel audit of unused / dependent objects (8 data sources) | Which items are safe to delete |
| 2 | [Optimize](02-optimize/prompt.md) | Data types, relationships, DAX, date table findings | Structural changes |
| 3 | [BPA](03-bpa/prompt.md) | Violations against AI-readiness rules | The fix backlog |
| 4 | [Describe](04-describe/prompt.md) | Draft descriptions + synonyms | Business accuracy |
| 5 | [Rename](05-rename/prompt.md) | Old → new rename map (+ hide keys, format strings) | The rename map |
| 6 | [Score](06-score/prompt.md) | Before/after AI-Readiness Score | The delta |

## How these map to the human ↔ agent workflow

| Workflow stage | Repo step(s) | Who |
|----------------|--------------|-----|
| **Analyze** | 1 Cleanup · 3 BPA | Agent (via MCP) |
| **Scope** | You set business context & rules | You |
| **Audit** | 2 Optimize · 4 Describe · 5 Rename (proposed) | Agent + skills |
| **Review** | Every step's proposed changes | You |
| **Auto-fix** | Apply approved changes to model + report | Agent (via MCP) |
| **Validate** | 6 Score + re-check | Agent + you |

> Golden rule: **you prompt, the agent builds, you approve.** Nothing is applied without your review.
