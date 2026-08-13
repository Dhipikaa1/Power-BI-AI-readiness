# Overview

**What this repo is:** a practical, prompt-driven method to turn any Power BI semantic model into
one that Copilot, Q&A, and AI agents can actually understand — plus a reproducible way to measure
how AI-ready a model is.

## Why AI-readiness matters

AI reads your model **literally**. Ask a Copilot data agent a question in plain English and it can
only answer well if the model's names, descriptions, and relationships make sense. Cryptic fields
like `cust_id` or `dt_ky` mean nothing to it, so answers come back weak or wrong.

## The idea in one line

**You prompt → the agent builds (via the Power BI Modeling MCP + skills) → you approve.**
Repeatable, reviewable, and measurable.

## What's inside

- [`steps/`](../steps/) — the 6 prompts (Cleanup → Optimize → BPA → Describe → Rename → Score).
- [`scoring/`](../scoring/) — a dependency-free AI-Readiness scorer (0–100).
- [`sample-model/`](../sample-model/) — a small before/after model in TMDL.
- [`docs/before-after.md`](before-after.md) — the measured results (0.0 → 98.1).
