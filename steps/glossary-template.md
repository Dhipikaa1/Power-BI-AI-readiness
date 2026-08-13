# Business Glossary (template)

The **Describe** (Step 4) and **Rename** (Step 5) prompts read this glossary to expand
abbreviations and ground names/descriptions in real business meaning — so the agent never
guesses. Copy this file, fill it in for your domain, and hand it to the agent with the prompt.

## Abbreviations

| Abbreviation | Means | Notes / usage |
|--------------|-------|---------------|
| `amt` | Amount | Monetary value (state currency) |
| `qty` | Quantity | Count of units |
| `txn` | Transaction | One order line / event |
| `cust` | Customer | Account that buys |
| `prod` | Product | Item sold |
| `dt` / `dte` | Date | Calendar date |
| `ky` / `id` | Key / Identifier | Surrogate key (usually hidden) |
| `fct` | Fact table | Transactional / numeric grain |
| `dim` | Dimension table | Descriptive lookup |
| `ytd` / `mtd` / `qtd` | Year / Month / Quarter to date | Time-intelligence |
| `disc` | Discount | Reduction on price |
| `seg` | Segment | Customer/market segment |

## Business terms & synonyms

| Canonical term | Synonyms users say | Definition |
|----------------|--------------------|-----------|
| Sales Amount | Revenue, Turnover, Sales | Gross sales value before tax |
| Customer | Client, Account, Buyer | The purchasing organization |
| Product | Item, SKU | The thing sold |

## Metric definitions (disambiguation)

| Metric | Definition | Not to be confused with |
|--------|-----------|--------------------------|
| Total Sales | `SUM('Fact Sales'[Sales Amount])` | Net Sales (after returns/discounts) |
| Average Discount % | Average of line-level discount rate | Total discount amount |

> Tip: the more precise this glossary, the safer and more consistent the generated
> descriptions and names. Keep contentious/ambiguous metrics here especially.
