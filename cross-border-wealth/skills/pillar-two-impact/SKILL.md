---
name: pillar-two-impact
description: >
  Assess the impact of OECD Pillar Two (Global Minimum Tax) on a cross-border
  structure. Calculates jurisdictional effective tax rates, identifies
  low-taxed constituent entities, models IIR/UTPR/QDMTT top-up liability, and
  recommends restructuring to minimize Pillar Two exposure while maintaining
  operational efficiency.
argument-hint: '[structure name | "full Pillar Two check" | specific entity | jurisdiction]'
tools:
  - westlaw_search_eu_law
  - westlaw_unified_search
  - web_search
categories:
  - tax
  - compliance
  - pillar-two
version: 0.1.0
---

# /pillar-two-impact

Assesses the impact of the OECD/G20 Pillar Two Global Minimum Tax framework on cross-border wealth structures. Identifies exposure, models top-up taxes, and recommends adjustments.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Determine scope.** From $ARGUMENTS:
   - Full Pillar Two assessment across all structures
   - Specific entity or jurisdiction assessment
   - "What if" modeling (what if jurisdiction X implements QDMTT?)

3. **Threshold check.** Pillar Two applies to MNE groups with consolidated revenue ≥ €750M in at least 2 of the preceding 4 fiscal years. For structures below this threshold:
   - Note the exemption but assess exposure if growth is expected
   - Flag jurisdictions that have enacted domestic minimum taxes regardless of the €750M threshold (e.g., some jurisdictions apply a domestic minimum tax to all companies)

4. **For each jurisdiction in the structure, assess:**

   ### A. Implementation Status
   Web search for current status using `references/pillar-two-tracker.md` as a starting point:
   - Has this jurisdiction enacted Pillar Two legislation?
   - Which rules are in force? (IIR, UTPR, QDMTT, or combinations)
   - Effective date
   - Any domestic variations or safe harbors?

   ### B. Jurisdictional Effective Tax Rate (ETR)
   For each constituent entity (CE), calculate the GloBE ETR:
   - **Adjusted covered taxes**: start with current income tax, adjust for:
     - Deferred tax adjustments
     - Uncertain tax position accruals
     - Withholding taxes (creditable vs. non-creditable)
     - Qualified refundable tax credits (excluded from numerator)
   - **GloBE income**: start with financial accounting income, adjust for:
     - Excluded dividends and equity gains (participation exemption analog)
     - International shipping income exclusion
     - Asymmetric foreign currency gains/losses
   - **ETR = Adjusted covered taxes / GloBE income**

   ### C. Top-Up Tax Calculation
   If jurisdictional ETR < 15%:
   - **Top-up tax percentage** = 15% − jurisdictional ETR
   - **Substance-based income exclusion (SBIE)**: 5% of eligible payroll + 5% of tangible asset carrying value (after transition period)
   - **Excess profit** = GloBE income − SBIE
   - **Top-up tax** = excess profit × top-up tax percentage

   ### D. Collection Mechanism
   - **QDMTT**: does the low-taxed jurisdiction impose its own top-up? (negates IIR/UTPR)
   - **IIR (Income Inclusion Rule)**: parent jurisdiction collects the top-up
   - **UTPR (Under-Taxed Profits Rule)**: peer jurisdictions share the top-up if no IIR applies

5. **Impact matrix:**

   | Jurisdiction | Entity | Current ETR | GloBE ETR | Below 15%? | Top-up | Collected by |
   |---|---|---|---|---|---|---|
   | [jurisdiction] | [entity] | [rate] | [rate] | [Yes/No] | [amount/estimate] | [QDMTT/IIR/UTPR] |

6. **Transitional safe harbors check:**
   - Simplified ETR ≥ 15% (based on CbCR data)?
   - De minimis exclusion (revenue < €10M AND income < €1M in the jurisdiction)?
   - Routine profits test (income ≤ SBIE)?

7. **Restructuring recommendations.** For entities below 15%:
   - **QDMTT play**: relocate to jurisdiction with a QDMTT (tax stays local)
   - **Substance increase**: increase payroll/tangible assets to maximize SBIE
   - **Regime change**: exit IP box or special regime to raise ETR above 15%
   - **Entity consolidation**: merge entities in same jurisdiction to blend ETRs
   - **Re-evaluate the structure**: if Pillar Two eliminates the benefit, simplify

   Tag each recommendation: 🟢 low complexity / 🟡 moderate / 🟠 complex / 🔴 fundamental restructuring

8. **Produce Pillar Two impact report:**
   - Executive summary (scope, threshold status, total top-up exposure)
   - Entity-by-entity analysis
   - Impact matrix
   - Safe harbor status
   - Restructuring options ranked by impact / effort
   - Timeline of upcoming Pillar Two changes by jurisdiction

9. **Offer next steps:**
   > 1. **Model a restructuring** — I'll recalculate the impact after [proposed change]
   > 2. **QDMTT deep dive** — detailed analysis of QDMTT in [jurisdiction]
   > 3. **Compare pre/post** — side-by-side of current structure vs. optimized structure
   > 4. **HTML report** — interactive Pillar Two dashboard
   > 5. **Monitor** — set up alerts for Pillar Two implementation changes
   > 6. **Something else**

## Verification

All Pillar Two implementation statuses are verified via web search. The GloBE Rules (Model Rules Dec 2021, Commentary Mar 2022, Administrative Guidance) and OECD Inclusive Framework updates are the authoritative references. Each data point is tagged with its source and date.
