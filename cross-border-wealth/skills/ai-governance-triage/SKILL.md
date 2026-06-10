---
name: ai-governance-triage
description: >
  Classify AI systems under the EU AI Act, identify prohibited practices, and
  assess high-risk AI system requirements. Maps compliance obligations and
  conformity assessment pathways.
argument-hint: '[AI system description | use case | "full classification"]'
tools:
  - westlaw_search_eu_law
  - westlaw_eu_compliance_search
  - westlaw_eu_compliance_article
  - web_search
categories:
  - ai-regulation
  - compliance
  - technology
version: 0.1.0
---

# /ai-governance-triage

Classifies AI systems under the EU AI Act risk framework and maps compliance obligations. Identifies prohibited practices, assesses high-risk system requirements, and determines the conformity assessment pathway.

## Downstream chain (EU AI Act P12)

This skill is the **entry point** of the EU AI Act deliverable chain. The risk class it produces feeds a fixed sequence of legal artifacts that ends in the disclosure text a marketing page must carry:

**risk-class (this skill) → conformity-assessment documentation (Art. 9–17/43 technical file + QMS) → `/cross-border-wealth:privacy-impact-assessment` (GDPR Art. 35 DPIA on the data flows) → `/cross-border-wealth:compliance-checker` (filing/registration obligations) → required Art. 50 transparency-disclosure text → handed to the Content-Gen plugin for the landing page.**

Carry the classification forward, do not re-derive it downstream: a 🟠 High-Risk or 🟡 Limited-Risk outcome here sets the conformity obligations and the Art. 50 disclosure that the later steps build on (e.g., chatbot, emotion-recognition, and deepfake/synthetic-content systems each require specific Art. 50 wording). The Legal steps own the *content* of each artifact and the disclosure text; **Content-Gen owns rendering it into the page** — never publish a regulated AI claim or ship the disclosure before Legal review passes. Orchestration sequences the steps; this skill only needs to know the chain exists and emit the classification the chain depends on.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Identify the AI system.** Gather:
   - What does the system do? (functional description)
   - Who deploys it? (provider vs. deployer distinction under the AI Act)
   - Where is it deployed? (EU market, EU-affecting, third country)
   - What decisions does it make or support?
   - Who is affected by its outputs?
   - What data does it use?
   - Is there human oversight in the loop?

3. **Prohibited practices check (Art. 5).** Screen for:
   - [ ] Subliminal manipulation causing harm
   - [ ] Exploitation of vulnerabilities (age, disability, social/economic situation)
   - [ ] Social scoring by public authorities
   - [ ] Real-time remote biometric identification in public spaces (law enforcement)
   - [ ] Untargeted scraping for facial recognition databases
   - [ ] Emotion recognition in workplace/education
   - [ ] Biometric categorization inferring sensitive attributes
   - [ ] Predictive policing based solely on profiling

   **If ANY box is checked → STOP. System is PROHIBITED. Advise immediately.**

4. **Risk classification:**

   ### 🔴 Unacceptable Risk (Art. 5)
   - Falls under prohibited practices above
   - **Action:** Cannot be placed on EU market. Full stop.

   ### 🟠 High Risk (Art. 6 + Annex III)
   - Biometric identification and categorization
   - Critical infrastructure management
   - Education and vocational training (access, assessment)
   - Employment (recruitment, promotion, termination, task allocation)
   - Essential services access (credit scoring, insurance, social benefits)
   - Law enforcement
   - Migration, asylum, border control
   - Administration of justice and democratic processes
   - Safety components of products under EU harmonization legislation
   - **Action:** Full compliance regime applies (see step 5)

   ### 🟡 Limited Risk (Art. 50)
   - Chatbots and conversational AI (transparency obligation)
   - Emotion recognition systems (disclosure obligation)
   - Deepfake/synthetic content generation (labeling obligation)
   - **Action:** Transparency obligations only

   ### 🟢 Minimal Risk
   - AI-enabled video games, spam filters, inventory management
   - **Action:** Voluntary codes of conduct; no mandatory requirements

5. **High-risk system requirements (if applicable):**

   | Requirement | Article | Status | Gap | Priority |
   |---|---|---|---|---|
   | Risk management system | Art. 9 | ❌ Not in place | Need continuous RMS | 🔴 Critical |
   | Data governance | Art. 10 | 🟡 Partial | Training data documentation incomplete | 🟠 High |
   | Technical documentation | Art. 11 | ❌ Not in place | Full technical file needed | 🔴 Critical |
   | Record-keeping / logging | Art. 12 | 🟡 Partial | Audit logs exist but not AI Act compliant | 🟡 Medium |
   | Transparency to deployers | Art. 13 | ❌ Not in place | Instructions for use needed | 🟠 High |
   | Human oversight | Art. 14 | 🟢 In place | Document oversight mechanism | 🟢 Low |
   | Accuracy, robustness, cybersecurity | Art. 15 | 🟡 Partial | Robustness testing needed | 🟠 High |
   | Quality management system | Art. 17 | ❌ Not in place | QMS for AI needed | 🔴 Critical |
   | EU Declaration of Conformity | Art. 47 | ❌ Not in place | Requires all above first | 🔴 Critical |
   | CE marking | Art. 48 | ❌ Not in place | After conformity assessment | 🟠 High |
   | Registration in EU database | Art. 49 | ❌ Not in place | After CE marking | 🟡 Medium |

6. **Conformity assessment pathway (Art. 43):**
   - Internal control (Annex VI) — for most high-risk systems
   - Third-party assessment (Annex VII) — for biometric systems and critical infrastructure
   - Determine which pathway applies
   - Timeline and cost estimate

7. **General-purpose AI model obligations (if applicable, Art. 51-56):**
   - Is this a GPAI model? (trained with large compute, general-purpose capability)
   - Systemic risk threshold: >10^25 FLOPs training compute
   - Obligations: technical documentation, downstream transparency, copyright compliance
   - Systemic risk additional: adversarial testing, incident reporting, model evaluation

8. **Compliance timeline:**
   - Prohibited practices: Already in force (Feb 2025)
   - GPAI obligations: Aug 2025
   - High-risk systems (Annex III): Aug 2026
   - Full application: Aug 2027 (products under harmonization legislation)

9. **Offer next steps:**
   > 1. **Compliance roadmap** — detailed implementation plan for high-risk requirements
   > 2. **Technical documentation** — I'll draft the Art. 11 technical file structure
   > 3. **Risk management system** — design the Art. 9 continuous RMS
   > 4. **FRIA** — Fundamental Rights Impact Assessment (Art. 27, for deployers)
   > 5. **Governance framework** — organizational AI governance structure
   > 6. **Run the deliverable chain** — DPIA (`/cross-border-wealth:privacy-impact-assessment`) → filings (`/cross-border-wealth:compliance-checker`) → Art. 50 disclosure text for the landing page (rendered by Content-Gen)
   > 7. **Something else**
