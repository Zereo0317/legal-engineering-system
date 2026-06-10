---
name: transfer-pricing-review
description: >
  Review an intercompany transaction or TP policy against the arm's-length
  standard. FAR analysis, methodology selection, comparability assessment,
  documentation gap check. Flags BEPS risks and cross-border mismatches.
argument-hint: '[transaction description | TP policy document | "review IP royalties from X to Y"]'
tools:
  - westlaw_search_cases
  - westlaw_get_case
  - westlaw_classic_search
  - westlaw_oecd_get_treaty
  - westlaw_oecd_model_convention
  - web_search
categories:
  - tax
  - compliance
version: 0.1.0
---

# /transfer-pricing-review

Reviews intercompany transactions and transfer pricing arrangements against the OECD arm's-length standard and local TP rules.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Get the transaction.** From $ARGUMENTS or ask: what's the intercompany transaction? (IP royalties, management fees, service charges, loans, inventory pricing, cost-sharing, etc.)

3. **Map the transaction:**
   - Parties (which entities, which jurisdictions)
   - Transaction type (services, IP, tangible goods, financial)
   - Direction and amount
   - Current pricing basis (if any)
   - Documentation status

4. **FAR Analysis** (Functions, Assets, Risks):
   - What functions does each party perform?
   - What assets does each party use or contribute?
   - What risks does each party assume?
   - Does the FAR analysis support the current allocation of profit?

5. **Methodology assessment:**
   - Which OECD method applies? (CUP, TNMM, Profit Split, Cost-Plus, Resale Minus)
   - Is the method applied correctly?
   - Are comparables available and appropriate?
   - Does the local jurisdiction require a specific method?

6. **Cross-border consistency check:**
   - Is what's deductible in Country A includible in Country B?
   - Are both jurisdictions applying the same method/arm's-length range?
   - Is there a mismatch that creates double taxation or double non-taxation?

7. **BEPS risk flags:**
   - BEPS Action 8-10: is the pricing consistent with value creation?
   - BEPS Action 13: CbCR, master file, local file — are they current?
   - Pillar Two impact: does the TP structure create low-taxed income?
   - Hard-to-value intangibles (HTVI): does the HTVI regime apply?

8. **Produce assessment** with the dual tag system:
   - 🟢 Arm's-length / 🟡 Needs documentation / 🟠 Pricing questionable / 🔴 Indefensible
   - Specific remediation for each finding

9. **Offer next steps:**
   > 1. **Fix the pricing** — I'll draft revised pricing with methodology and documentation
   > 2. **Benchmark study** — I'll outline a comparability analysis
   > 3. **Case research** — I'll find TP cases in [jurisdiction] on [issue]
   > 4. **APA assessment** — I'll evaluate whether an Advance Pricing Agreement makes sense
   > 5. **HTML report** — formatted TP review with risk matrix
