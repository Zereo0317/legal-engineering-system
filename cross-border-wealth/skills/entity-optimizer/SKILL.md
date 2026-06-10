---
name: entity-optimizer
description: >
  Given a goal (hold IP, hold investments, preserve wealth, operate a business),
  recommend the optimal entity type and jurisdiction. Compares LLCs, trusts,
  foundations, VCCs, SPCs, partnerships, and corporate forms. Considers tax,
  substance, privacy, succession, and cost.
argument-hint: '[goal | "hold IP in Asia" | "investment vehicle for family office" | "succession planning"]'
tools:
  - westlaw_search_cases
  - westlaw_search_eu_law
  - web_search
categories:
  - structuring
  - tax
version: 0.1.0
---

# /entity-optimizer

Recommends the optimal legal vehicle for a specific purpose. Each entity type is a building block — this skill helps you pick the right one.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Clarify the goal.** What does the entity need to do?
   - Hold equity participations (passive holding)
   - Hold and license IP (patents, trademarks, software, know-how)
   - Hold and manage investments (securities, funds, alternatives)
   - Conduct operations (employees, customers, revenue)
   - Preserve and transfer wealth (succession, asset protection)
   - Hold real estate
   - Treasury / cash management
   - Joint venture / co-investment vehicle
   - Philanthropic / charitable purpose

3. **Assess entity types** for the stated goal:

   | Vehicle | Best for | Key advantage | Key risk |
   |---|---|---|---|
   | Company (Ltd/Corp/AG/BV) | Operations, holding | Limited liability, familiar | Double taxation, public disclosure |
   | LLC / LLP | Operations, flexibility | Pass-through taxation, flexible governance | Not recognized in all jurisdictions |
   | Trust (discretionary) | Wealth preservation, succession | Separation of control from benefit | Trustee risk, jurisdiction-dependent |
   | Trust (purpose) | Specific purposes, orphan structures | No beneficiaries = no beneficial owner | Limited flexibility |
   | Foundation (private) | Wealth preservation, civil law alternative to trusts | Legal personality + settlor-like flexibility | Not available everywhere |
   | VCC / SPC | Investment management, multi-strategy | Segregated portfolios, single registration | Newer vehicle, limited case law |
   | Partnership (LP/GP) | Funds, joint ventures | Pass-through, flexible allocation | GP liability, registration requirements |
   | Branch | Market entry, PE planning | No separate entity, simpler | PE exposure, limited liability unclear |
   | Protected Cell Company | Captive insurance, structured products | Asset segregation within single entity | Jurisdiction-specific |

4. **For each recommended vehicle, analyze:**
   - Tax treatment in the jurisdiction of formation AND in the client's primary jurisdictions
   - Treaty access (can this entity type access treaties?)
   - Substance requirements
   - Privacy and disclosure obligations
   - Governance (who controls, who has fiduciary duties, who has information rights)
   - Succession / continuity (what happens when the founder dies)
   - Setup cost and timeline
   - Ongoing maintenance cost
   - Exit flexibility (how easy to unwind, migrate, or convert)

5. **Recommend with rationale.** Top 2-3 options ranked by fit for the stated goal, considering the practice profile's risk posture and existing structure.

6. **Offer next steps:**

   > **What next?**
   > 1. **Design the entity** — I'll draft the formation specifications (jurisdiction, governance, capitalization)
   > 2. **Connect to existing structure** — I'll show how [recommended vehicle] fits into your current structure
   > 3. **Jurisdiction scan** — I'll compare jurisdictions for this vehicle type
   > 4. **Case research** — I'll find cases on [vehicle type] in [jurisdiction]
   > 5. **Something else**
