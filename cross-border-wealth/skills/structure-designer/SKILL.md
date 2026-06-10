---
name: structure-designer
description: >
  Given a goal and constraints, design a cross-border structure from scratch.
  Selects jurisdictions, entity types, flow routing, and treaty paths to build
  an optimized architecture. The inverse of structure-analysis — builds instead
  of auditing. Produces a complete blueprint with diagrams, cost estimates,
  substance requirements, and implementation timeline.
argument-hint: '[goal | "IP holding for SaaS" | "family succession across 3 jurisdictions" | "investment platform for UHNW"]'
tools:
  - westlaw_classic_search
  - westlaw_unified_search
  - web_search
categories:
  - structuring
  - design
  - tax-planning
version: 0.1.0
---

# /structure-designer

Designs a cross-border wealth structure from scratch given a goal, constraints, and risk posture. The builder skill — where structure-analysis audits what exists, structure-designer creates what should exist.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`. If placeholders present, stop: "Run `/cross-border-wealth:cold-start-interview` first."

2. **Clarify the design brief.** From $ARGUMENTS or ask:

   **Goal:** What is this structure for?
   - IP holding and licensing (patents, trademarks, software, know-how)
   - Investment management (securities, PE/VC, real estate, crypto)
   - Operational holding (group treasury, management, shared services)
   - Wealth preservation and succession (generational transfer, asset protection)
   - Joint venture / co-investment (multi-party, multi-jurisdiction)
   - Real estate portfolio (multi-country, mixed residential/commercial)
   - Founder liquidity event (pre-IPO structuring, exit optimization)
   - Charitable / philanthropic (private foundation, donor-advised fund)

   **Constraints:**
   - Source jurisdictions (where income arises)
   - Residence jurisdictions (where beneficiaries are tax resident)
   - Budget for setup and maintenance
   - Risk tolerance (conservative / moderate / aggressive)
   - Timeline (when must this be operational?)
   - Existing entities to incorporate (or greenfield?)

3. **Design the structure.** Apply the Legal Engineering methodology:

   ### Step A: Identify the Optimal Path
   - Map the income flows from source to ultimate beneficiary
   - Identify all border crossings where tax applies
   - Calculate the "direct holding" baseline (no intermediate entities)
   - Determine the theoretical minimum tax achievable through treaty routing

   ### Step B: Select Jurisdictions
   For each layer of the structure, evaluate candidate jurisdictions:

   | Layer | Purpose | Candidates | Selection criteria |
   |---|---|---|---|
   | Operating | Income generation | Source jurisdiction(s) | Where customers/assets are |
   | IP | License to operating entities | IE, NL, LU, SG, CH | IP box rate, treaty network, substance cost |
   | Holding | Equity in operating + IP | NL, LU, SG, HK, UAE | Participation exemption, WHT, treaty access |
   | Trust/Foundation | Wealth preservation | BVI, Cayman, JE, LI, SD | Trust law quality, privacy, succession |
   | Treasury | Cash management | LU, NL, SG, IE | Interest deductibility, WHT, pooling |

   Use `/cross-border-wealth:jurisdiction-scanner` data and `references/jurisdiction-profiles.md`.

   ### Step C: Select Entity Types
   For each jurisdiction, recommend the optimal vehicle:
   - Corporate form (BV, Ltd, AG, Pte Ltd, LLC)
   - Trust form (discretionary, purpose, VISTA, STAR, directed)
   - Foundation form (Stiftung, private foundation)
   - Fund form (VCC, SPC, ICAV, LP, SCSp)
   - Branch (when PE planning is needed)

   ### Step D: Route the Flows
   For each cross-border payment:
   - Type (dividend, interest, royalty, service fee, management charge)
   - Treaty rate at each border crossing
   - Transfer pricing methodology and arm's-length basis
   - Deductibility in source / includibility in destination
   - LOB/PPT eligibility at each intermediate entity

   Use `/cross-border-wealth:treaty-mapper` logic for routing optimization.

   ### Step E: Substance Specification
   For each entity, specify the minimum substance required:
   - Number and type of employees
   - Office requirements (physical, virtual, serviced)
   - Director residency and qualifications
   - Decision-making location (board meetings, key decisions)
   - Documentation requirements
   - Estimated annual cost of maintaining substance

   ### Step F: Compliance Impact
   - CRS/FATCA classification for each entity
   - DAC6 hallmark analysis for the overall arrangement
   - BEPS CbCR applicability
   - UBO register filings
   - Local TP documentation requirements

4. **Produce the blueprint.** Format:

   **Executive Summary** (5-7 sentences: what, why, cost, timeline, risk level)

   **Structure Diagram** (ASCII, showing entities, jurisdictions, ownership, flows with treaty rates)

   ```
   Example:
   UBO (TW tax resident)
        │ 100% settlor
   BVI Discretionary Trust
   (protector: UBO, trustee: licensed trust co)
        │ 100% beneficiary corp
   SG HoldCo (Pte Ltd)
   (3 employees, local directors, substance)
        │                    │
   IE IP Co (Ltd)        NL Treasury BV
   (KDB 10%, 5 staff)   (innovation box 9%)
        │ royalty @ 0% (EU IRD)
   US OpCo (LLC)
   (100 employees, revenue)
   ```

   **Layer-by-Layer Specification** (jurisdiction, entity type, purpose, substance, cost)

   **Flow Analysis** (each cross-border payment with treaty basis, WHT rate, TP methodology)

   **Cost Estimate** (setup costs + annual maintenance per entity)

   **Risk Assessment** (per-dimension scores using 🟢/🟡/🟠/🔴)

   **Implementation Timeline** (sequenced: which entities to form first, migration plan if applicable)

   **Exit Analysis** (what it costs to unwind each layer)

5. **Offer next steps:**

   > **What next?**
   > 1. **Stress test** — I'll run a full risk assessment on this design
   > 2. **Treaty verification** — I'll verify every treaty rate against current treaty text
   > 3. **Compare alternatives** — I'll design 2 alternative structures and compare
   > 4. **Implementation plan** — detailed timeline with formation documents, regulatory filings
   > 5. **HTML report** — interactive blueprint with diagrams, flow maps, cost tables
   > 6. **Case research** — I'll find cases on [relevant issue] in [relevant jurisdiction]
   > 7. **Something else**

## Verification

Every jurisdiction selection, treaty rate, tax rate, substance requirement, and entity recommendation is verified via web search against current sources. Each is tagged with provenance. The reviewer note reflects the verification coverage.
