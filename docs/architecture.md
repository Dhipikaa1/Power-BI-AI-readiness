# Architecture

```
                 You (business context + approval)
                              │  prompts
                              ▼
                   GitHub Copilot (agent)
                              │  tool calls
              ┌───────────────┴───────────────┐
              ▼                               ▼
   Power BI Modeling MCP                 Reusable skills
   (inspect / edit model,               (naming, descriptions,
    run DAX, export TMDL)                relationship & BPA rules)
              │                               │
              └───────────────┬───────────────┘
                              ▼
             Semantic model  +  PBIP report
                              │
                              ▼
                 AI-Readiness Score (0–100)
```

## Flow

1. **Analyze** — the agent inspects the model (Cleanup + BPA) via MCP.
2. **Scope** — you provide business context and rules.
3. **Audit** — the agent drafts Optimize / Describe / Rename changes using MCP + skills.
4. **Review** — you approve every proposed change.
5. **Auto-fix** — the agent applies approved changes to the model and the PBIP report.
6. **Validate** — the scorer computes the AI-Readiness Score; iterate on the lowest rules.

## Design principles

- **Prompt-driven, not black-box.** Every change is proposed, reviewed, and version-controlled.
- **Human-in-the-loop.** The agent never applies changes without approval.
- **Measurable.** The score is computed from model metadata by a simple, auditable rule set.
