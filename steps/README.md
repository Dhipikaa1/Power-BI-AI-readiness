# The 6 Steps

Each step is **prompt-driven**: you run the prompt with **GitHub Copilot (agent mode)** against your
model through the **Power BI Modeling MCP** (or paste it into your LLM of choice). You review the
proposed changes, then approve — the agent applies them to the model (and, where relevant, the report).

| # | Step | What it does | You review |
|---|------|--------------|-----------|
| 1 | [Cleanup](01-cleanup/prompt.md) | Find dead measures, hidden-but-unused columns, orphan tables | Deletions |
| 2 | [Optimize](02-optimize/prompt.md) | Simplify DAX, fix relationships, set data types | Model changes |
| 3 | [BPA](03-bpa/prompt.md) | Run AI-readiness Best Practice rules | Violations list |
| 4 | [Describe](04-describe/prompt.md) | Generate descriptions + synonyms for tables/columns/measures | Descriptions |
| 5 | [Rename](05-rename/prompt.md) | Business-friendly names; hide keys; set format strings | Rename map |
| 6 | [Score](06-score/prompt.md) | Compute the AI-Readiness Score (0–100) | Before/after report |

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
