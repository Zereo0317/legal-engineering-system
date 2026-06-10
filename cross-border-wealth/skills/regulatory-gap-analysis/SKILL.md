---
name: regulatory-gap-analysis
description: >
  Identify regulatory gaps, compliance shortfalls, and policy misalignments
  across jurisdictions. Compares current state against FATF, CRS, AEOI,
  Pillar Two, substance rules, and other regulatory frameworks.
argument-hint: '[framework | jurisdiction pair | "full compliance scan"]'
tools:
  - westlaw_search_eu_law
  - westlaw_eu_compliance_search
  - westlaw_eu_compliance_article
  - westlaw_search_regulations
  - web_search
categories:
  - compliance
  - regulatory
  - gap-analysis
version: 0.1.0
---

# /regulatory-gap-analysis

Identifies gaps between your current compliance posture and regulatory requirements across multiple jurisdictions. Produces a prioritized remediation roadmap with severity classification and jurisdiction-by-jurisdiction comparison.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Scope the analysis.** Determine:
   - Which regulatory frameworks to assess against:
     - FATF Recommendations (AML/CFT)
     - CRS (Common Reporting Standard)
     - AEOI (Automatic Exchange of Information)
     - Pillar Two / GloBE Rules (minimum tax)
     - Economic substance requirements
     - DAC6/MDR (Mandatory Disclosure Rules)
     - ATAD I/II/III (Anti-Tax Avoidance Directives)
     - Local regulatory requirements
   - Which jurisdictions are in scope
   - What is the entity/structure being assessed
   - Current compliance state (what's already in place)

3. **For each framework × jurisdiction, assess:**

   ### Requirement Mapping
   - What does the regulation require? (specific obligations)
   - What is currently in place? (current state)
   - What is the gap? (delta between requirement and reality)

   ### Gap Severity Classification
   - 🔴 **Critical** — Non-compliance creates immediate legal exposure (fines, penalties, criminal liability)
   - 🟠 **High** — Material gap that must be addressed within 90 days; regulatory risk if audited
   - 🟡 **Medium** — Gap exists but risk of enforcement is moderate; 6-month remediation timeline acceptable
   - 🟢 **Low** — Best-practice gap; no immediate regulatory risk but should be addressed in normal course

4. **Jurisdiction comparison matrix:**

   | Requirement | Jurisdiction A | Jurisdiction B | Jurisdiction C | Strictest Standard |
   |---|---|---|---|---|
   | Substance (employees) | ≥2 FTE | ≥1 qualified | No specific rule | Jurisdiction A |
   | Substance (premises) | Dedicated office | Registered address OK | Virtual OK | Jurisdiction A |
   | Reporting (CRS) | Full CRS | CRS + local additions | Non-CRS (but FATCA) | Jurisdiction B |
   | Transfer pricing docs | Full TP study | Summary TP doc | No requirement <€X | Jurisdiction A |
   | UBO register | Public register | Private register | No register | Jurisdiction A |

5. **Gap inventory:**

   | # | Framework | Jurisdiction | Gap Description | Severity | Deadline | Remediation Cost |
   |---|---|---|---|---|---|---|
   | G-001 | CRS | [Country] | Missing controlling person documentation | 🔴 Critical | Immediate | Low |
   | G-002 | Pillar Two | [Country] | No QDMTT filing prepared | 🟠 High | FY2025 | Medium |
   | ... | ... | ... | ... | ... | ... | ... |

6. **Remediation roadmap.** Prioritized by:
   - Severity (critical first)
   - Deadline proximity
   - Interdependencies (some fixes enable others)
   - Cost-effectiveness (quick wins first)

   ### Immediate (0-30 days)
   - Gap G-001: [specific remediation steps]
   - Gap G-003: [specific remediation steps]

   ### Short-term (30-90 days)
   - Gap G-002: [specific remediation steps]

   ### Medium-term (90-180 days)
   - Gap G-005: [specific remediation steps]

7. **Regulatory horizon scan.** Identify upcoming changes that will CREATE new gaps:
   - Pillar Two implementation timelines by jurisdiction
   - ATAD III / Unshell Directive
   - CRS 2.0 / Crypto-Asset Reporting Framework (CARF)
   - FATF Travel Rule expansion
   - Local legislative proposals

8. **Offer next steps:**
   > 1. **Remediate** — I'll draft specific policies/documents to close gap [G-XXX]
   > 2. **Deep dive** — detailed analysis of [specific framework] requirements
   > 3. **Restructure** — propose structural changes to eliminate multiple gaps
   > 4. **Monitor** — set up regulatory change tracking for your jurisdictions
   > 5. **Compliance calendar** — deadlines and filing dates for all requirements
   > 6. **Something else**
