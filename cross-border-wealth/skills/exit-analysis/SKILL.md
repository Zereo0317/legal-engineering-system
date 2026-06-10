---
name: exit-analysis
description: >
  Analyze the tax and legal consequences of unwinding, restructuring, or
  migrating a cross-border structure. Covers exit taxes, deemed disposals,
  clawbacks, liquidation sequences, entity migration, and treaty implications
  of restructuring. The "how do we get out?" skill.
argument-hint: '[structure name | "exit from X" | "migrate entity to Y" | "full unwind analysis"]'
tools:
  - westlaw_classic_search
  - westlaw_unified_search
  - web_search
categories:
  - tax-planning
  - restructuring
  - exit
version: 0.1.0
---

# /exit-analysis

Analyzes the consequences of unwinding, migrating, or fundamentally restructuring cross-border wealth structures. Exits are harder than entries — this skill maps every cost, trigger, and sequence.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Determine the exit scenario.** From $ARGUMENTS:
   - **Full unwind**: liquidate and dissolve all entities, repatriate assets
   - **Partial restructuring**: remove or replace specific entities/layers
   - **Entity migration**: re-domicile an entity from jurisdiction A to B
   - **Change of residence**: UBO relocating to a different jurisdiction
   - **Succession event**: death/incapacity of UBO or key person
   - **Regulatory trigger**: forced restructuring due to law change
   - **Sale/divestiture**: selling part of the structure to a third party

3. **Map exit triggers and costs for each entity:**

   ### A. Exit Taxes
   - **Corporate exit tax**: deemed disposal at market value on departure?
   - **Capital gains**: unrealized gains crystallized on liquidation/migration?
   - **Withholding tax**: distributions on liquidation treated as dividends?
   - **Clawbacks**: IP regime benefits, tax credits, grants that must be repaid?
   - **Stamp duty/transfer tax**: triggered by asset transfers during restructuring?

   ### B. Deemed Disposals
   For each jurisdiction where entities exist:
   - Does migration trigger a deemed disposal at market value?
   - Is there an exit tax installment plan (e.g., EU ATAD exit tax with 5-year payment option)?
   - What's the step-up basis in the receiving jurisdiction?
   - CFC implications: does dissolution trigger deemed income in the parent jurisdiction?

   ### C. Trust-Specific Exit Issues
   For trusts and foundations:
   - Is the trust revocable (simpler exit) or irrevocable (complex)?
   - Protector powers: can the protector force a distribution?
   - Trustee obligations on termination (final accounting, beneficiary notifications)
   - Exit charges in the trust jurisdiction?
   - Beneficiary tax consequences of receiving trust distributions?

   ### D. Liquidation Sequence
   The order matters:
   - Bottom-up: operating entities first, then holding companies, then trusts
   - Tax-optimized: which entities should be dissolved first to minimize cascading taxes?
   - Regulatory: which entities have regulatory obligations that constrain the sequence?
   - Contractual: loan covenants, guarantees, cross-default provisions

   ```
   Example sequence:
   1. US OpCo: distribute retained earnings to IE IP Co (WHT: 5% under treaty)
   2. IE IP Co: license termination, final royalty settlement
   3. IE IP Co: liquidation distribution to SG HoldCo (WHT: 0% under EU PSD)
   4. NL Treasury BV: repay intercompany loans, close bank accounts
   5. SG HoldCo: final distribution to BVI Trust (WHT: 0%)
   6. BVI Trust: distribution to beneficiaries (no BVI exit tax)
   7. Deregister entities in reverse order of dependency
   ```

   ### E. Treaty Implications of Restructuring
   - Do treaty benefits survive restructuring?
   - Does migration create treaty residence conflicts?
   - Are there anti-abuse provisions triggered by restructuring?
   - Does a change of beneficial owner invalidate existing treaty positions?

   ### F. Compliance Wind-Down
   - Final tax returns in each jurisdiction
   - CRS/FATCA deregistration
   - UBO register updates
   - DAC6 reporting for the restructuring itself
   - Deregistration from company/trust registers

4. **Cost the exit.** Produce an exit cost table:

   | Entity | Jurisdiction | Exit tax | WHT on distributions | Professional fees | Regulatory | Total |
   |---|---|---|---|---|---|---|
   | [entity] | [jurisdiction] | [amount/estimate] | [amount] | [estimate] | [filings] | [total] |
   | **Total exit cost** | | | | | | **[grand total]** |

5. **Timeline the exit.** Produce a phased timeline:

   | Phase | Duration | Actions | Dependencies |
   |---|---|---|---|
   | 1. Preparation | [weeks] | Valuations, legal opinions, board resolutions | None |
   | 2. Intra-group settlements | [weeks] | Loan repayments, royalty settlements | Phase 1 |
   | 3. Operating entity exits | [weeks] | Employee matters, customer contracts | Phase 2 |
   | 4. Holding layer liquidations | [weeks] | Distributions, deregistrations | Phase 3 |
   | 5. Trust/foundation termination | [weeks] | Final distributions, trustee discharge | Phase 4 |
   | 6. Compliance wind-down | [weeks] | Final returns, deregistrations | Phase 5 |

6. **Alternative scenarios.** Model at least two exit approaches:
   - **Minimum cost**: optimize for lowest total exit tax
   - **Minimum time**: fastest path to full unwind
   - **Partial retention**: keep the valuable parts, exit the rest

7. **Produce exit analysis report:**
   - Executive summary (total exit cost, recommended approach, timeline)
   - Entity-by-entity exit tax analysis
   - Liquidation sequence diagram
   - Cost table
   - Timeline
   - Alternative scenarios comparison

8. **Offer next steps:**
   > 1. **Implement Phase 1** — I'll draft the board resolutions and engagement letters
   > 2. **Deep dive on exit tax** — full analysis of [jurisdiction]'s exit tax rules
   > 3. **Case research** — I'll find cases on exit taxes / deemed disposals in [jurisdiction]
   > 4. **Restructure instead** — I'll design a new structure that avoids the exit costs
   > 5. **HTML report** — interactive exit analysis with timeline and cost breakdown
   > 6. **Something else**

## Verification

Exit tax rules, deemed disposal provisions, and WHT rates on liquidation distributions are verified via web search and Westlaw Classic for each relevant jurisdiction. The analysis is jurisdiction-specific throughout — a rule from one jurisdiction is never silently applied to another.
