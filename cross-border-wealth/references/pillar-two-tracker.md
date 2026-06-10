# Pillar Two (Global Minimum Tax) — Implementation Tracker

> **What this document covers:** OECD/G20 Inclusive Framework Pillar Two establishes a
> global minimum effective tax rate of 15% for large multinational enterprise (MNE) groups.
> This tracker maps the legislative status of Pillar Two implementation across jurisdictions
> relevant to cross-border wealth structuring, offshore holding, trust planning, and fund
> structures. It is maintained as a reference for the legal-engineering plugin's
> jurisdiction-selection and structure-validation modules.
>
> **Data reliability:** All entries below are tagged `[model knowledge — verify]`. Pillar Two
> legislation is evolving rapidly. Before relying on any status for client advice, verify
> current status via OECD Inclusive Framework updates, local government gazettes, or a web
> search for the specific jurisdiction.

---

## 1. Framework Overview

| Element | Detail |
|---|---|
| **Minimum rate** | 15% global minimum effective tax rate (GloBE rules) |
| **In-scope groups** | MNE groups with consolidated annual revenue >= EUR 750M in at least 2 of the prior 4 fiscal years |
| **IIR (Income Inclusion Rule)** | Top-up tax charged to the UPE (or intermediate parent) on the low-taxed income of constituent entities in other jurisdictions |
| **UTPR (Under-Taxed Profits Rule)** | Backstop — denies deductions or requires equivalent adjustment where the IIR has not been applied; allocated by substance (employees + tangible assets) |
| **QDMTT (Qualified Domestic Minimum Top-up Tax)** | Domestic top-up tax enacted by the source jurisdiction itself, which takes priority over IIR/UTPR and keeps revenue onshore |
| **STTR (Subject to Tax Rule)** | Treaty-based rule (separate from GloBE) allowing source countries to impose limited withholding on related-party payments taxed below 9% |

**Key timeline:**

- Dec 2021 — OECD Model GloBE Rules published
- Mar 2022 — Commentary on the GloBE Rules
- Dec 2022 — EU Minimum Tax Directive (2022/2523) adopted
- Feb 2023 — OECD Administrative Guidance (first tranche)
- Jul 2023 — Additional Administrative Guidance + GloBE Information Return
- 2024-2026 — Ongoing Administrative Guidance, safe-harbor refinements, STTR MLI

---

## 2. Implementation Status by Jurisdiction

`[model knowledge — verify]` — Status as understood for early-to-mid 2026.

### 2.1 Key Structuring Jurisdictions

| Jurisdiction | IIR | UTPR | QDMTT | Effective Date | Legislative Status | Notes |
|---|---|---|---|---|---|---|
| **Netherlands** | In force | In force | In force | FY 2024 (IIR/QDMTT); FY 2025 (UTPR) | Enacted (Wet minimumbelasting 2024) | QDMTT designed to be "qualifying" under OECD standards |
| **Luxembourg** | In force | In force | In force | FY 2024 (IIR/QDMTT); FY 2025 (UTPR) | Enacted (Dec 2023 law) | Key holding jurisdiction; IP regime interaction noted |
| **Singapore** | In force | Not yet | In force | FY 2025 | Enacted (MTT Act 2024) | QDMTT ("DTT") enacted; IIR via MTT; refundable investment credits introduced to maintain competitiveness |
| **Hong Kong** | In force | Not yet | In force | FY 2025 | Enacted (GMTT Ordinance 2024) | QDMTT ("DMTT") enacted; IIR adopted; UTPR deferred |
| **Ireland** | In force | In force | In force | FY 2024 (IIR/QDMTT); FY 2025 (UTPR) | Enacted (Finance Act 2023, S.111A TCA) | 15% rate replaces prior 12.5% for in-scope groups; KDB interaction significant |
| **UAE** | Not yet | Not yet | In force | FY 2025 | QDMTT enacted (Cabinet Decision 2024); IIR/UTPR under review | DMTT at 15%; free-zone regime interaction is critical |
| **Switzerland** | In force | Not yet | In force | FY 2024 | Enacted (constitutional amendment + ordinance) | QDMTT adopted; 75% of QDMTT revenue to cantons, 25% to Confederation; UTPR deferred |
| **United Kingdom** | In force | In force | Enacted | FY 2024 (IIR); FY 2025 (UTPR) | Enacted (Finance Act 2023 / FA 2024) | Multinational Top-up Tax (IIR) + UTPR; domestic top-up tax enacted |
| **Germany** | In force | In force | Not yet | FY 2024 (IIR); FY 2025 (UTPR) | Enacted (MinStG, Dec 2023) | No standalone QDMTT; relies on existing CIT rate (~30%) being above 15% |
| **France** | In force | In force | Not yet | FY 2024 (IIR); FY 2025 (UTPR) | Enacted (Finance Law 2024) | Domestic rate well above 15%; no separate QDMTT needed |
| **Japan** | In force | Not yet | In force | FY 2024 (IIR); FY 2025 (QDMTT) | Enacted (2023 & 2024 tax reform laws) | IIR first adopted in Asia-Pacific; UTPR timing TBD |
| **South Korea** | In force | Proposed | In force | FY 2024 (IIR); FY 2025 (QDMTT) | Enacted (International Tax Adjustment Act amendments) | UTPR legislation pending |
| **Australia** | In force | In force | In force | FY 2024 | Enacted (Treasury Laws Amendment 2024) | All three rules enacted; QDMTT ensures domestic collection |
| **Canada** | In force | Proposed | In force | FY 2024 (IIR/QDMTT) | Global Minimum Tax Act enacted (Jun 2024) | UTPR deferred to FY 2025/2026; DST interaction noted |

### 2.2 Offshore / Trust Jurisdictions

| Jurisdiction | IIR | UTPR | QDMTT | Effective Date | Legislative Status | Notes |
|---|---|---|---|---|---|---|
| **BVI** | N/A | N/A | Not yet | — | No legislation | Zero-tax jurisdiction; entities will be subject to top-up tax via parent jurisdiction's IIR/UTPR |
| **Cayman Islands** | N/A | N/A | Not yet | — | No legislation | Same position as BVI; no domestic income tax regime to build QDMTT on |
| **Jersey** | N/A | N/A | In force | FY 2025 | Enacted (Taxation (Pillar Two) (Jersey) Law 2024) | QDMTT at 15% for in-scope MNEs; standard 0% rate otherwise preserved |
| **Guernsey** | N/A | N/A | In force | FY 2025 | Enacted (2024 legislation) | QDMTT introduced similarly to Jersey; preserves 0% standard rate |
| **Bermuda** | N/A | N/A | In force | FY 2025 | Enacted (Corporate Income Tax Act 2023) | 15% CIT for in-scope MNEs; first income tax in Bermuda history |
| **Liechtenstein** | In force | Not yet | In force | FY 2024 | Enacted (implementing EU Directive via EEA) | EEA member; follows EU Directive timeline |

### 2.3 Other Major Economies

| Jurisdiction | IIR | UTPR | QDMTT | Effective Date | Legislative Status | Notes |
|---|---|---|---|---|---|---|
| **United States** | N/A | N/A | N/A | — | Not adopted | US has GILTI (13.125%/16.406%) + CAMT (15% book minimum); not Pillar Two conforming but interaction via OECD safe harbors |
| **China** | Consultation | Not yet | Consultation | TBD | Draft rules circulated | Expected adoption; existing 25% CIT well above 15% for most entities |
| **India** | Consultation | Not yet | Proposed | TBD | Under review | Likely to prioritize QDMTT + STTR; domestic rates already above 15% |
| **Brazil** | Not yet | Not yet | In force | FY 2025 | QDMTT enacted (Dec 2024 legislation) | 15% domestic minimum top-up tax enacted; IIR/UTPR timing uncertain |

---

## 3. Key Design Choices by Jurisdiction

`[model knowledge — verify]`

### 3.1 QDMTT Design Variations

| Jurisdiction | QDMTT Basis | Key Design Choice |
|---|---|---|
| **Netherlands** | GloBE rules (accounting-based) | Closely tracks OECD model; full substance-based income exclusion (SBIE) applied |
| **Singapore** | GloBE rules | DTT is OECD-conforming; introduced refundable tax credits for qualifying economic activities to offset top-up |
| **Hong Kong** | GloBE rules | DMTT mirrors OECD; interacts with existing concessionary regimes (offshore claims) |
| **UAE** | GloBE rules | DMTT applies to free-zone and mainland entities; designed to preserve Qualifying Free Zone Person benefits below the 750M threshold |
| **Jersey/Guernsey** | GloBE rules | Narrow scope — only in-scope MNEs pay; 0% rate preserved for everyone else |
| **Bermuda** | Corporate income tax (new) | Full 15% CIT for in-scope groups; not a narrow top-up but a new income tax |
| **Switzerland** | GloBE rules | Cantonal implementation; 75/25 revenue split (canton/Confederation); existing cantonal rate variations remain for below-threshold groups |

### 3.2 Interaction with Existing Regimes

| Regime | Interaction |
|---|---|
| **US GILTI** | GILTI uses a blended per-country approach only after 2025 TCJA changes (if enacted). Current GILTI may not fully eliminate IIR exposure. OECD has provided a transitional GILTI safe harbor (limited period). |
| **US CAMT** | 15% corporate alternative minimum tax on adjusted financial statement income; not a GloBE-qualifying QDMTT but may reduce effective top-up in practice |
| **EU Anti-Tax Avoidance Directives** | ATAD I/II (CFC, hybrid mismatch) continue to apply alongside Pillar Two; stacking effects possible |
| **Existing CFC rules** | Jurisdictions with CFC rules (UK, Germany, Japan, Australia) must coordinate CFC tax with GloBE computations to avoid double counting |

### 3.3 Notable Carve-outs and Safe Harbors Beyond OECD Baseline

- **Singapore:** Refundable investment credits (RIC) framework allows qualifying credits to reduce Pillar Two top-up tax without creating low ETR
- **Hong Kong:** Clarified that offshore-sourced income not brought into HK is still captured for GloBE ETR computation (aligning with substance requirements)
- **Switzerland:** Cantons retain ability to offer targeted subsidies/grants that are structured to be GloBE-compatible (not reducing covered taxes)

---

## 4. Transitional Safe Harbors

`[model knowledge — verify]`

| Safe Harbor | Description | Period |
|---|---|---|
| **CbCR Safe Harbor** | Simplified ETR test using existing Country-by-Country Report data. Three tests: (1) de minimis, (2) simplified ETR >= 15%, (3) routine profits. If any test met, top-up tax = zero for that jurisdiction. | FY starting on/before 31 Dec 2026, but no later than 30 Jun 2028 |
| **De Minimis Exclusion** | Permanent: jurisdictional top-up tax = zero if (a) average GloBE revenue < EUR 10M AND (b) average GloBE income < EUR 1M | Permanent (built into GloBE rules) |
| **SBIE (Substance-Based Income Exclusion)** | Carve-out equal to 5% of tangible asset carrying value + 5% of eligible payroll costs (after transition: 8%/10% declining to 5%/5% over 10 years) | Transitional rates for FY 2024-2032; full 5%/5% from FY 2033 |
| **QDMTT Safe Harbor** | Where a jurisdiction's QDMTT meets OECD qualifying standards, IIR/UTPR top-up for that jurisdiction = zero (avoids double computation) | Permanent once QDMTT is confirmed as "qualifying" by OECD peer review |
| **Transitional CbCR Filing** | Simplified GloBE Information Return for early years | Expected through FY 2026 reporting |

---

## 5. Impact on Common Structures

`[model knowledge — verify]`

### 5.1 IP Box Regimes

| Regime | Pre-Pillar Two Rate | Pillar Two Impact |
|---|---|---|
| **Ireland KDB** | 10% (raised from 6.25% in 2024) | In-scope groups: KDB income now subject to top-up to 15%. KDB benefit reduced from ~5pp saving to zero for covered groups. Below-threshold groups unaffected. |
| **Netherlands Innovation Box** | 9% | Top-up tax applies; effective benefit drops from ~16pp saving (25%-9%) to ~10pp (25%-15%). Still some benefit from Innovation Box + SBIE interaction. |
| **Luxembourg IP Regime** | ~5.2% (80% exemption) | Fully caught by Pillar Two for in-scope groups. Effective rate topped up to 15%. |
| **Singapore IDI** | 5-10% (concessionary) | Topped up to 15%; Singapore's refundable investment credits partially offset the increase for qualifying R&D expenditure. |

### 5.2 Free Zone Regimes

- **UAE QFZP:** Qualifying Free Zone Persons with 0% CIT on qualifying income will face 15% DMTT if part of in-scope MNE group. Below-threshold groups retain 0%. The DMTT effectively neutralizes the free-zone benefit for large MNEs.
- **Other free zones** (various jurisdictions): Any preferential rate below 15% is topped up. The competitive advantage of free zones shifts from tax rate to non-tax factors (infrastructure, regulation, talent).

### 5.3 Offshore Holding Structures

- **BVI/Cayman holding companies:** Zero-tax entities will generate full 15% top-up tax at the parent level (via IIR) or at sister-entity level (via UTPR). SBIE may offset some top-up if the entity has real substance (employees + tangible assets), but pure holding entities with minimal substance receive minimal SBIE.
- **Interposed holding layers:** Multiple offshore layers no longer provide incremental tax benefit for in-scope groups. Simplification of holding structures is expected.
- **Below-threshold groups:** Structures for MNE groups below EUR 750M revenue remain unaffected by Pillar Two (but may be caught by domestic CFC/anti-avoidance rules).

### 5.4 Fund Structures

- **Excluded entities:** Investment funds and real estate investment vehicles that are Ultimate Parent Entities (UPEs) are generally excluded from GloBE if they meet the definition of an "Excluded Entity" (e.g., regulated fund, >80% held by qualifying investors, no trading activity).
- **Fund-owned portfolio companies:** Where a fund owns a portfolio company that itself exceeds EUR 750M consolidated revenue, that portfolio group is in scope independently.
- **Pension funds:** Generally excluded as UPEs. But pension fund subsidiaries engaged in active business may be constituent entities of an in-scope MNE group.
- **Sovereign wealth funds:** Excluded entities under the GloBE rules (governmental entities exclusion).

---

## 6. Monitoring Checklist

For ongoing tracker maintenance, verify the following at least quarterly:

- [ ] OECD Inclusive Framework outcome statements and Administrative Guidance updates
- [ ] EU Directive transposition status for remaining member states
- [ ] US legislative developments (TCJA extension, GILTI reform, potential Pillar Two adoption)
- [ ] China and India formal adoption timelines
- [ ] OECD peer review of QDMTT "qualifying" status for each jurisdiction
- [ ] Transitional safe harbor expiry and extension decisions
- [ ] CbCR Safe Harbor — data availability and filing deadlines

---

*Last reviewed: `[model knowledge — verify]` May 2026. All entries require independent verification against current legislation and OECD guidance before use in client advice.*
