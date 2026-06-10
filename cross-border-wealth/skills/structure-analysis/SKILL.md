---
name: structure-analysis
description: >
  Analyze a cross-border wealth structure — entities, flows, treaties, substance,
  TP, compliance. Paste an org chart, describe it, or point at a document. Produces
  a scored assessment with optimization opportunities. The core skill of the legal
  engineering optimizer.
argument-hint: '[paste structure | file path | Drive link | "describe my structure"]'
tools:
  - westlaw_search_cases
  - westlaw_search_eu_law
  - westlaw_classic_search
  - westlaw_oecd_get_treaty
  - web_search
categories:
  - structuring
  - tax
  - compliance
version: 0.1.0
---

# /structure-analysis

Analyzes a multi-jurisdiction wealth structure for tax efficiency, defensibility, substance adequacy, treaty eligibility, transfer pricing compliance, and regulatory exposure. Produces a scored assessment with optimization opportunities.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`. If placeholders present, stop: "Run `/cross-border-wealth:cold-start-interview` first — I need to know your jurisdiction footprint and risk posture."

2. **Get the structure.** From $ARGUMENTS: file path, Drive link, pasted text, or verbal description. If none provided, ask: "Describe your structure — entities, jurisdictions, ownership, and the main flows (dividends, royalties, service fees, management charges). An org chart, a narrative, or even a sketch all work."

3. **Map the structure.** Build a complete model:

   **Entities:** For each entity, record:
   - Legal form (company, trust, foundation, LLC, VCC, partnership, branch)
   - Jurisdiction of incorporation/establishment
   - Jurisdiction of tax residence (may differ from incorporation)
   - Substance indicators (employees, office, directors, decision-making location)
   - Purpose in the structure (holding, operating, IP, treasury, trust, conduit)

   **Ownership:** Map the full ownership chain from ultimate beneficial owner(s) to operating entities. Note: trusts don't have "owners" — map settlor, trustee, protector, beneficiaries.

   **Flows:** Map every cross-border payment:
   - Type (dividend, interest, royalty, service fee, management charge, capital contribution, loan)
   - Direction (from entity A to entity B)
   - Treaty relied upon (if any) and applicable withholding rate
   - Transfer pricing basis (arm's-length methodology)
   - Deductibility in source jurisdiction / includibility in recipient jurisdiction

4. **Draw the diagram.** Produce an ASCII structure diagram showing entities, jurisdictions, ownership lines, and flow arrows. Label each flow with its type and treaty rate.

5. **Run the analysis.** Apply six assessment dimensions:

   ### A. Tax Efficiency Analysis
   - Calculate the effective tax rate on income flowing from source to ultimate beneficiary
   - Identify each "tax touchpoint" (border crossing where tax or withholding applies)
   - Compare to the "direct holding" baseline (what would the tax be if the ultimate beneficiary held the operating entity directly?)
   - Efficiency score: net tax saved / compliance cost

   ### B. Substance Assessment
   For each entity, apply the jurisdiction's substance requirements:
   - OECD BEPS Action 5 (substantial activities requirement for IP regimes)
   - EU ATAD III / Unshell Directive (minimum substance indicators)
   - Local substance rules (e.g., Cayman ES Act, BVI ES Act, UAE substance rules)
   - The "tax inspector test": what would an inspector find at this address?

   Tag each entity: ✅ Adequate substance | ⚠️ Marginal | ❌ Insufficient | ❓ Cannot assess

   ### C. Treaty Eligibility
   For each treaty benefit claimed:
   - LOB (Limitation on Benefits) test — does the entity qualify?
   - PPT (Principal Purpose Test) — would a reasonable person conclude the arrangement's principal purpose was obtaining the treaty benefit?
   - Beneficial ownership — is the entity the beneficial owner of the income, or a conduit?
   - Treaty residence — is the entity actually resident in the treaty jurisdiction?

   Tag each treaty claim: ✅ Defensible | ⚠️ Challengeable | ❌ Likely denied | ❓ Cannot assess

   ### D. Transfer Pricing
   For each intercompany transaction:
   - What TP methodology applies? (CUP, TNMM, profit split, cost-plus, resale-minus)
   - Is there documentation?
   - Does the pricing match the functions performed, assets used, and risks assumed (FAR analysis)?
   - Cross-check: is what's deductible in Country A actually includible in Country B?

   Tag each transaction: ✅ Arm's-length | ⚠️ Needs documentation | ❌ Pricing indefensible | ❓ Cannot assess

   ### E. Compliance Exposure
   - CRS/FATCA: which entities are reporting financial institutions? What gets reported where?
   - DAC6: does this structure contain hallmarks? Is it a reportable arrangement?
   - BEPS CbCR: does the group exceed the €750M threshold?
   - UBO registers: where are beneficial owners disclosed?
   - Local requirements: any jurisdiction-specific reporting?

   ### F. Exit Analysis
   - What happens if the client wants to unwind this structure?
   - Exit taxes in each jurisdiction (deemed disposal, capital gains, clawbacks)
   - Migration options (can entities re-domicile?)
   - Liquidation sequence (which entities must be wound up first?)

6. **Score the structure.** Overall and per-dimension, using:
   - 🟢 **Sound** — well-structured, defensible, efficient
   - 🟡 **Adequate** — works but has improvement opportunities
   - 🟠 **Vulnerable** — significant risks that should be addressed
   - 🔴 **Critical** — structural issues requiring immediate attention

7. **Identify optimization opportunities.** For each vulnerability or inefficiency found, propose a specific fix:
   - What to change (add substance, reroute a flow, replace an entity, restructure ownership)
   - Expected improvement (tax saving, risk reduction, compliance simplification)
   - Implementation complexity (simple / moderate / complex / requires external counsel)
   - Transition cost (exit taxes, restructuring fees, regulatory filings)

8. **Produce the deliverable.** Format as a structured analysis with:
   - Executive summary (3-5 sentences: what the structure does, overall score, top 3 findings)
   - Structure diagram
   - Dimension-by-dimension assessment with tags and citations
   - Optimization roadmap (prioritized by impact / effort)
   - Decision tree

9. **Offer next steps:**

   > **What next? Pick one and I'll help you build it out:**
   > 1. **Optimize** — I'll redesign the [weakest dimension] with a concrete restructuring proposal
   > 2. **Deep dive** — pick a dimension and I'll do a jurisdiction-by-jurisdiction deep analysis
   > 3. **HTML report** — I'll generate an interactive report with structure diagrams and risk heat maps
   > 4. **Treaty mapper** — I'll map the full treaty network and find better routing paths
   > 5. **Compliance check** — I'll run a full DAC6/CRS/FATCA compliance assessment
   > 6. **Case research** — I'll find the landmark cases in [relevant jurisdiction] on [relevant issue]
   > 7. **Something else** — tell me what you'd do with this

## Verification

Every legal proposition in the output is sourced. Treaty rates are verified against the treaty text or a current treaty database. Tax rates are verified against current legislation. Substance requirements are verified against the relevant jurisdiction's current rules. If a position cannot be verified, it's tagged `[model knowledge — verify]` and the reviewer note reflects it.
