---
name: risk-assessment
description: >
  Identify vulnerabilities in a cross-border structure — substance challenges,
  treaty shopping exposure, GAAR risk, recharacterization, upcoming regulatory
  changes, and the "what keeps you up at night" analysis. Cross-skill synthesis
  that pulls from structure-analysis, treaty-mapper, and compliance-checker.
argument-hint: '[structure name | "full risk scan" | specific risk type]'
tools:
  - westlaw_search_cases
  - westlaw_search_eu_law
  - westlaw_classic_search
  - web_search
categories:
  - tax
  - compliance
  - structuring
version: 0.1.0
---

# /risk-assessment

Identifies vulnerabilities in a cross-border wealth structure. The "stress test" skill — what could go wrong, how likely is it, and what's the exposure?

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Scope the assessment.** Full scan or specific risk type:
   - Substance challenge risk
   - Treaty shopping / PPT challenge
   - GAAR (General Anti-Avoidance Rule) exposure
   - Transfer pricing adjustment risk
   - Recharacterization risk (entity reclassification, flow recharacterization)
   - Regulatory change risk (upcoming law changes that affect the structure)
   - Pillar Two / minimum tax impact
   - Exit / unwind risk
   - Succession / key person risk
   - Reputational risk

3. **For each risk dimension, assess:**
   - **Likelihood:** How likely is this to be challenged? (Low / Medium / High / Near-certain)
   - **Impact:** If challenged, what's the financial exposure? (quantify if possible)
   - **Detectability:** How likely are the authorities to find this? (CRS/FATCA reporting, public registers, audit triggers)
   - **Precedent:** Are there cases where similar structures were challenged? (reference the Star Atlas)
   - **Trend:** Is this risk increasing or decreasing? (OECD initiatives, local legislative changes)

4. **Risk heat map:**

   | Risk | Likelihood | Impact | Detectability | Overall | Trend |
   |---|---|---|---|---|---|
   | Substance challenge (Entity X) | 🟠 High | 🔴 €XXM | 🟡 Medium | 🔴 Critical | ↑ Increasing |
   | PPT denial (Treaty A-B) | 🟡 Medium | 🟠 €XXM | 🟢 Low | 🟠 Elevated | ↑ Increasing |
   | ... | ... | ... | ... | ... | ... |

5. **Upcoming changes scan.** Web search for regulatory changes affecting the structure:
   - Pillar Two implementation status in each jurisdiction
   - ATAD III / Unshell Directive timeline
   - Local CFC rule changes
   - Treaty renegotiations
   - GAAR expansion
   - Substance requirement tightening

6. **Produce risk report** with:
   - Executive summary (top 3 risks, overall risk posture)
   - Risk-by-risk analysis with citations
   - Heat map
   - Mitigation options for each material risk
   - Timeline of upcoming changes

7. **Offer next steps:**
   > 1. **Mitigate** — I'll design specific fixes for the top [N] risks
   > 2. **Restructure** — I'll propose an alternative structure that reduces [specific risk]
   > 3. **Case research** — I'll find cases where [similar risk] was litigated
   > 4. **Monitor** — I'll set up a watch list for regulatory changes affecting your structure
   > 5. **HTML report** — risk dashboard with heat map and mitigation tracker
   > 6. **Something else**
