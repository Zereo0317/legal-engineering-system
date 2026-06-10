---
name: immigration-pathway
description: >
  Analyze immigration options and design the optimal pathway to citizenship,
  permanent residence, or work authorization. Covers investor programs, skilled
  worker routes, points systems, leverage strategies, and cost optimization.
  The "how do I become a citizen of X for less?" skill.
argument-hint: '[target country] [target status: citizenship | PR | work permit] or "Singapore citizenship as tech professional"'
tools:
  - westlaw_search_legislation
  - westlaw_search_regulations
  - westlaw_unified_search
  - web_search
categories:
  - immigration
  - citizenship
  - regulatory-arbitrage
version: 0.1.0
---

# /immigration-pathway

Designs the optimal immigration pathway, treating immigration systems as regulatory modules with specific inputs (money, skills, time, connections) and outputs (residency, work rights, citizenship). Finds the path that maximizes your leverage while minimizing cost and time.

## Instructions

1. **Load pathway profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`.

2. **Clarify the target.** From $ARGUMENTS:
   - **Target country**: Where do you want status?
   - **Target status**: Citizenship / Permanent Residence / Work Permit / Long-term visa
   - **Optimization**: Cheapest? Fastest? Least disruptive to current life?
   - **Leverage**: What advantages do you have? (Tech skills, capital, education, nationality, employer)

3. **Load reference data.** Read the relevant reference file:
   - Singapore: `legal-pathways/references/singapore-immigration.md`
   - Use web search to verify current requirements

4. **Map ALL available pathways to the target status:**

   For each pathway, assess:

   ### A. Eligibility
   - Who qualifies? (Nationality restrictions, age, education, experience, capital)
   - Does the applicant qualify based on their profile?
   - What's missing?

   ### B. Cost Structure
   - Direct costs (application fees, investment amounts, legal fees)
   - Indirect costs (required purchases, mandatory spending, bonds)
   - Opportunity costs (must live there X years, can't work elsewhere)
   - Ongoing costs (minimum spend, tax obligations, renewal fees)

   ### C. Timeline
   - Application processing time
   - Required residence period before next step
   - Total time from start to target status
   - Expedited options

   ### D. Conditions and Obligations
   - Physical presence requirements
   - Employment requirements
   - Investment maintenance period
   - Tax obligations triggered
   - Military/national service obligations
   - Citizenship renunciation requirements (does target country allow dual citizenship?)

   ### E. Strategic Value
   - Passport strength (visa-free countries)
   - Tax treaty network
   - Business environment
   - Quality of life factors
   - Path to other jurisdictions (does this citizenship unlock others?)

5. **Leverage analysis.** Identify what the applicant has that the target country wants:

   | Leverage | What you have | What they want | How to position it |
   |---|---|---|---|
   | Skills | [e.g., AI/ML expertise] | [e.g., Singapore's Smart Nation agenda] | [e.g., Apply through Tech.Pass or EP in AI sector] |
   | Capital | [e.g., $500K savings] | [e.g., Investment in local economy] | [e.g., GIP Fund option or startup investment] |
   | Network | [e.g., connections to TW tech ecosystem] | [e.g., Bridge to Greater China market] | [e.g., Position as cross-border tech bridge] |
   | Education | [e.g., Top university degree] | [e.g., COMPASS points for qualifications] | [e.g., Maximize COMPASS scoring] |

6. **"Face engineering" and condition exchange analysis.** For each pathway:
   - What symbolic contributions increase approval probability?
   - What community involvement or public positioning helps?
   - What reciprocal value can you offer beyond minimum requirements?
   - How to build a narrative that aligns with the country's strategic priorities
   - Timing: when to apply for maximum advantage (election cycles, policy windows)

7. **Produce pathway comparison matrix:**

   | Pathway | Eligibility | Cost | Timeline | Conditions | Success rate | Risk |
   |---|---|---|---|---|---|---|
   | [Pathway A] | [Met/Not met/Partial] | [Total cost] | [Months/Years] | [Key conditions] | [Est. %] | [Key risks] |
   | [Pathway B] | ... | ... | ... | ... | ... | ... |

8. **Design the recommended SOP:**

   | Phase | Action | Timeline | Cost | Dependencies | CTA |
   |---|---|---|---|---|---|
   | 0. Preparation | [Credential evaluation, document gathering] | Months 1-2 | [cost] | None | Start NOW |
   | 1. Entry | [Visa application, job search, investment] | Months 3-6 | [cost] | Phase 0 | [specific action] |
   | 2. Status building | [Work, integrate, meet conditions] | Months 7-24 | [cost] | Phase 1 | [specific action] |
   | 3. PR application | [Compile dossier, apply] | Month 25+ | [cost] | Phase 2 | [specific action] |
   | 4. Citizenship | [Meet PR duration, apply] | Year 4+ | [cost] | Phase 3 | [specific action] |

9. **Risk assessment:**
   - Policy change risk (immigration policy is politically volatile)
   - Rejection risk and appeal options
   - Dual citizenship complications
   - Tax implications of gaining new citizenship/PR
   - Military/national service obligations
   - What happens if you fail at each stage — fallback plan

10. **Cross-border wealth structuring connection.** Flag when immigration decisions interact with wealth structuring:
    - Tax residence changes triggering exit taxes
    - CRS/FATCA reporting changes
    - Treaty benefits gained or lost
    - Entity restructuring needed
    - Suggest `/cross-border-wealth:exit-analysis` or `/cross-border-wealth:structure-analysis` where relevant

11. **Offer next steps:**
    > **What next?**
    > 1. **Deep dive on [recommended pathway]** — full regulatory analysis with case law
    > 2. **Visa application strategy** — optimize your application for maximum approval odds
    > 3. **Tax impact analysis** — how does this immigration move affect your tax position?
    > 4. **Timeline builder** — detailed month-by-month action plan
    > 5. **Leverage optimization** — how to strengthen your application profile before applying
    > 6. **Something else**

## Verification

Immigration requirements are verified via web search against official government sources (ICA for Singapore, USCIS for US, etc.). Immigration law changes frequently — every requirement is tagged with source and verification date. Processing times are estimates based on recent publicly reported data. Success rates are approximations based on published statistics where available.
