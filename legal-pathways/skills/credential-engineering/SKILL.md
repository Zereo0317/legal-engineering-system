---
name: credential-engineering
description: >
  Analyze credential gaps and design the optimal pathway to obtain professional
  licenses across borders. Covers education gap analysis, credential evaluation,
  exam preparation, supervised hours planning, and visa strategy. The
  "how do I get licensed in X as a foreigner?" skill.
argument-hint: '[target credential] [target jurisdiction] or "US counselor license with foreign psychology degree"'
tools:
  - westlaw_search_regulations
  - westlaw_get_cfr_section
  - westlaw_search_legislation
  - westlaw_unified_search
  - web_search
categories:
  - professional-licensing
  - credentials
  - immigration
version: 0.1.0
---

# /credential-engineering

Designs the complete pathway from your current qualifications to a target professional license in another jurisdiction. Treats licensing boards as regulatory modules — each has specific inputs (degrees, hours, exams) and outputs (licenses, privileges).

## Instructions

1. **Load pathway profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`. If not populated, suggest running `/legal-pathways:cold-start-interview` first.

2. **Identify the target credential.** From $ARGUMENTS or profile:
   - Target license type (e.g., LPC, LMHC, LCSW, Licensed Psychologist, PE, CPA)
   - Target jurisdiction (e.g., specific US state, UK, Australia, Singapore)
   - If not clear, ask.

3. **Load reference data.** Read the relevant reference file:
   - US counselor licensing: `legal-pathways/references/us-counselor-licensing.md`
   - Citizenship/investment: `legal-pathways/references/citizenship-investment-matrix.md`
   - Use web search to verify current requirements (licensing boards update annually)

4. **Map current qualifications against target requirements.** Build a gap matrix:

   ### A. Education Requirements
   - Degree level required vs. held (e.g., Master's required, Bachelor's held)
   - Credit hours required vs. completed (e.g., 60 graduate credits required)
   - Specific coursework required (e.g., 8 core CACREP areas)
   - Accreditation requirements (e.g., CACREP-accredited program required vs. preferred)
   - Foreign degree equivalency (does the target board accept foreign degrees?)

   ### B. Credential Evaluation
   - Which evaluation service is required? (WES, ECE, NACES member, board-specific)
   - General evaluation vs. course-by-course evaluation
   - Timeline and cost for evaluation
   - Common issues with degrees from the applicant's country

   ### C. Supervised Experience
   - Total hours required (e.g., 2,000-4,000 for LPC)
   - Direct client contact hours required
   - Supervisor qualifications required
   - Can hours from home country count? (with evaluation)
   - Post-degree vs. post-Master's requirements

   ### D. Examinations
   - Which exams are required? (NCE, NCMHCE, EPPP, state-specific)
   - Eligibility requirements to sit for exam
   - Pass rates and preparation timeline
   - Can you take the exam before completing all other requirements?

   ### E. Legal Status / Immigration
   - Visa required to study (F-1, student visa)
   - Visa required to complete supervised hours (OPT, H-1B, work permit)
   - Visa required to practice after licensure
   - Does the credential itself provide immigration benefits?

   ### F. Language Requirements
   - English proficiency requirements (TOEFL, IELTS minimum scores)
   - Any state-specific language requirements

5. **Produce the gap analysis matrix:**

   | Requirement | Target | Current | Gap | Severity | Cost to close | Time to close |
   |---|---|---|---|---|---|---|
   | Degree level | Master's (60 cr) | Bachelor's (128 cr) | Need Master's | Critical | $15K-60K | 2-3 years |
   | CACREP accreditation | Required/preferred | N/A | Need CACREP program | Critical | included | included |
   | ... | ... | ... | ... | ... | ... | ... |

6. **Design the optimal pathway.** Considering budget, timeline, and risk tolerance, recommend:

   ### Pathway Option A: [Fastest]
   - Step-by-step SOP with timeline
   - Total cost breakdown
   - Risk assessment

   ### Pathway Option B: [Cheapest]
   - Step-by-step SOP with timeline
   - Total cost breakdown
   - Risk assessment

   ### Pathway Option C: [Most Reliable]
   - Step-by-step SOP with timeline
   - Total cost breakdown
   - Risk assessment

7. **For each pathway, produce a detailed SOP:**

   | Step | Action | Timeline | Cost | Dependencies | CTA |
   |---|---|---|---|---|---|
   | 1 | Credential evaluation (WES/ECE) | Weeks 1-8 | $200-350 | Transcripts from home university | Order transcripts NOW |
   | 2 | Apply to CACREP program | Months 2-4 | $50-100 app fee | Credential evaluation complete | Research programs NOW |
   | ... | ... | ... | ... | ... | ... |

8. **Jurisdiction shopping analysis.** If the user is flexible on jurisdiction:
   - Which states/jurisdictions have the lowest barriers for foreign-educated applicants?
   - Which accept non-CACREP programs?
   - Which have credential transfer/reciprocity with other jurisdictions?
   - Which provide the fastest path to independent practice?

9. **Offer next steps:**
   > **What next?**
   > 1. **Deep dive on [recommended jurisdiction]** — full regulatory analysis
   > 2. **Program comparison** — I'll compare specific degree programs for your situation
   > 3. **Visa strategy** — immigration pathway to study and practice
   > 4. **Case research** — find precedent for credential recognition from your country
   > 5. **Timeline builder** — interactive Gantt-style timeline with milestones
   > 6. **Something else**

## Verification

All licensing requirements are verified via web search against the relevant licensing board's official website. Requirements change frequently — every data point is tagged with its source and verification date. State-specific requirements reference the relevant state statute or administrative code (via eCFR/Westlaw where applicable).

## Reference: Common Professional Licensing Domains

| Domain | US License | Typical requirements | Key governing body |
|---|---|---|---|
| Mental health counseling | LPC / LMHC / LCPC | Master's (48-60 cr) + 2,000-4,000 hrs + NCE/NCMHCE | State licensing board + NBCC |
| Clinical social work | LCSW | MSW (60 cr) + 3,000-4,000 hrs + ASWB exam | State board + ASWB |
| Psychology | Licensed Psychologist | Doctoral (PhD/PsyD) + 1,500-2,000 hrs + EPPP | State board + ASPPB |
| Marriage & family therapy | LMFT | Master's (60 cr) + 2,000-4,000 hrs + MFT exam | State board + AAMFT |
| Engineering | PE (Professional Engineer) | BS + 4 yrs experience + FE + PE exam | State board + NCEES |
| Accounting | CPA | 150 credit hours + experience + CPA exam | State board + AICPA/NASBA |
