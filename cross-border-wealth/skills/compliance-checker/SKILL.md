---
name: compliance-checker
description: >
  Check a structure against DAC6, CRS, FATCA, BEPS CbCR, UBO registers, and
  local reporting obligations. Identifies reportable arrangements, filing
  deadlines, and gaps. The "are we compliant?" skill.
argument-hint: '[structure name | "full check" | specific regime | jurisdiction]'
tools:
  - westlaw_search_eu_law
  - westlaw_eu_compliance_search
  - westlaw_eu_compliance_article
  - web_search
  - web_fetch
categories:
  - compliance
  - tax
  - reporting
version: 0.1.0
---

# /compliance-checker

Checks a cross-border structure against international and local reporting obligations. Identifies what must be reported, where, by when, and by whom.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Scope the check.** From $ARGUMENTS:
   - Full check: assess all regimes against all structures in the profile
   - Specific regime: just DAC6, just CRS, just FATCA, etc.
   - Specific structure: check one structure against all regimes
   - Specific jurisdiction: what's required in [jurisdiction]?

3. **For each applicable regime:**

   ### DAC6 (EU Mandatory Disclosure)
   - Does the arrangement have hallmarks? (Category A-E)
   - Is the main benefit test satisfied? (Categories A and B require it; C-E don't)
   - Who is the intermediary? (adviser, or is the taxpayer self-reporting?)
   - 30-day filing deadline from trigger event
   - Which EU Member State receives the report?
   - Legal professional privilege: does the intermediary benefit from it? (narrow scope per C-623/22 — System 10)

   ### CRS (Common Reporting Standard)
   - Which entities are Reporting Financial Institutions?
   - Which accounts are Reportable Accounts?
   - What's reported: account balance, income, gross proceeds
   - Reporting jurisdiction and counterpart jurisdiction
   - Due diligence: self-certification status

   ### FATCA
   - Which entities are FFIs (Foreign Financial Institutions)?
   - Which are NFFEs (Non-Financial Foreign Entities)?
   - Active vs. passive NFFE classification
   - US person identification
   - IGA Model 1 vs. Model 2 — which applies?

   ### BEPS Country-by-Country Reporting
   - Does the group exceed the €750M revenue threshold?
   - Which entity is the reporting entity?
   - Where is the CbCR filed?
   - What data is disclosed (revenue, profit, tax, employees by jurisdiction)?

   ### UBO Registers
   - Where are UBO registers applicable?
   - Who qualifies as a UBO? (>25% ownership, control, beneficiary)
   - Public vs. restricted access
   - Filing deadlines and update obligations

   ### Local TP Documentation
   - Which jurisdictions require TP documentation?
   - Master file / local file requirements
   - Filing vs. preparation obligations
   - Contemporaneous documentation requirement

4. **Produce compliance matrix:**

   | Regime | Applies? | Status | Filing deadline | Gap |
   |---|---|---|---|---|
   | DAC6 | [Yes/No] | [Filed/Pending/Overdue/N/A] | [date] | [description of gap] |
   | CRS | ... | ... | ... | ... |
   | ... | ... | ... | ... | ... |

5. **Flag gaps and risks:**
   - ⏰ Overdue filings
   - ⚠️ Missing self-certifications
   - 🔴 Reportable arrangements not yet reported
   - 📋 Documentation that should exist but doesn't

6. **Offer next steps:**
   > 1. **Fix gaps** — I'll draft the missing filings or documentation
   > 2. **DAC6 deep dive** — full hallmark analysis for [arrangement]
   > 3. **Compliance calendar** — I'll build a calendar of all deadlines
   > 4. **HTML report** — compliance dashboard with status indicators
   > 5. **Something else**
