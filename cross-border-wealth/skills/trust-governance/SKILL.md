---
name: trust-governance
description: >
  Analyze trust structures — fiduciary duties, protector powers, no-contest
  clauses, trustee liability, beneficiary rights, VCC sub-fund governance.
  Spans common-law trusts, civil-law foundations, and hybrid vehicles.
  References the Star Atlas cases on trust litigation.
argument-hint: '[trust document | governance question | "review trust deed" | "protector powers"]'
tools:
  - westlaw_search_cases
  - westlaw_get_case
  - westlaw_search_singapore_cases
  - westlaw_get_singapore_judgment
  - westlaw_classic_search
  - web_search
categories:
  - structuring
  - litigation
version: 0.1.0
---

# /trust-governance

Analyzes trust and foundation governance. Covers fiduciary duties, protector powers, no-contest clauses, trustee liability, beneficiary rights, and the emerging VCC/fund governance space.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Determine the question.** From $ARGUMENTS:
   - Review a trust deed / foundation charter for governance issues
   - Analyze a specific governance question (protector powers, trustee removal, etc.)
   - Assess trustee liability risk
   - Review a no-contest / in terrorem clause
   - Analyze arbitration clause enforceability for trust disputes
   - VCC / fund governance analysis

3. **Apply jurisdiction-specific analysis.** Trust law varies dramatically:
   - **Common law** (BVI, Cayman, Jersey, Singapore, England, US states): equitable duties, Saunders v Vautier, Hastings-Bass
   - **Civil law** (Liechtenstein foundation, Dutch STAK, Curaçao foundation): legal personality, charter governance
   - **Hybrid** (Singapore VCC, Cayman SPC): statutory framework overlaying trust/corporate principles
   - **US state-specific** (South Dakota, Nevada, Delaware, New Hampshire): directed trusts, trust protectors, dynasty trusts

4. **Star Atlas cross-references.** Flag relevant cases:
   - **System 03** (Carlson v. Colangelo): no-contest clause — enforce/construe vs. contest/nullify
   - **System 04** (Credit Suisse v. Ivanishvili): trustee fiduciary duty, "hypothetical properly-managed portfolio" damages
   - **System 11** (Zhong Shan v. RG Strategy Fund VCC): VCC sub-fund winding up
   - **System 12** (Pinnacle v. McTaggart): arbitration of non-signatory beneficiary, statutory fiduciary duty
   - **System 13** (McArthur v. McArthur): trust arbitration clause, consent problem

5. **Produce governance assessment** covering:
   - Fiduciary duty analysis (duty of care, duty of loyalty, duty of good faith, duty to inform)
   - Power allocation (trustee, protector, investment adviser, trust committee)
   - Beneficiary rights and information entitlements
   - Dispute resolution mechanism (court, arbitration, mediation)
   - Succession planning (what happens when the settlor dies, when the protector dies)
   - Exit mechanisms (trust termination, variation, migration)

6. **Offer next steps:**
   > 1. **Draft provisions** — I'll draft governance clauses for [specific issue]
   > 2. **Case research** — I'll find cases on [trust issue] in [jurisdiction]
   > 3. **Compare jurisdictions** — I'll compare trust law across [jurisdictions]
   > 4. **Risk assessment** — I'll assess trustee liability exposure
   > 5. **HTML report** — governance analysis with case references
