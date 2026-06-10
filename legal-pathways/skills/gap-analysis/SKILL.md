---
name: gap-analysis
description: >
  General gap identification across any regulatory domain. Compares what you
  have against what you need for any target credential, license, or status.
  Produces a prioritized gap matrix with cost, timeline, and CTAs.
argument-hint: '[target credential or status] or "full analysis of all targets"'
tools:
  - web_search
categories:
  - analysis
  - planning
version: 0.1.0
---

# /gap-analysis

Identifies every gap between where you are and where you want to be, across all target credentials in your profile. Produces a unified gap matrix that feeds into the specialized skills.

## Instructions

1. **Load pathway profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`. If not populated, suggest running `/legal-pathways:cold-start-interview`.

2. **Scope the analysis.** From $ARGUMENTS:
   - **Full analysis**: assess all targets in the profile
   - **Specific target**: analyze gaps for one credential/status
   - **Specific domain**: just education gaps, just experience gaps, etc.

3. **For each target credential/status, assess these gap categories:**

   ### Education Gaps
   - Degree level (Bachelor's → Master's → Doctoral)
   - Credit hours (total and subject-specific)
   - Accreditation (CACREP, ABET, AACSB, etc.)
   - Specific courses required but not completed
   - Foreign degree equivalency status

   ### Experience Gaps
   - Total professional experience years
   - Supervised clinical/professional hours
   - Specific experience types required
   - Jurisdiction-specific experience requirements

   ### Examination Gaps
   - Required exams not yet passed
   - Eligibility to sit for required exams
   - Prerequisite courses for exam eligibility

   ### Language Gaps
   - English proficiency (TOEFL/IELTS scores vs. requirements)
   - Other language requirements

   ### Legal Status Gaps
   - Visa/immigration status needed vs. current
   - Work authorization requirements
   - Residency requirements

   ### Financial Gaps
   - Budget vs. estimated total cost
   - Funding sources available
   - Financial requirements for visa/immigration

   ### Documentation Gaps
   - Credential evaluations needed
   - Transcripts to obtain
   - Background checks required
   - References/recommendations needed

4. **Produce the unified gap matrix:**

   | # | Gap | Target | Category | Severity | Cost | Time | Blocks |
   |---|---|---|---|---|---|---|---|
   | 1 | No Master's degree | US LPC | Education | Critical | $15K-60K | 2-3 yrs | Everything |
   | 2 | No credential evaluation | US LPC | Documentation | Critical | $200-350 | 6-8 wks | Program admission |
   | 3 | No supervised hours | US LPC | Experience | Critical | $0 (part of program) | 1-2 yrs | Licensure |
   | ... | ... | ... | ... | ... | ... | ... | ... |

   Severity levels:
   - **Critical** — cannot proceed without closing this gap
   - **Major** — significantly delays or complicates the pathway
   - **Minor** — can be addressed in parallel or is a nice-to-have

5. **Dependency analysis.** Map which gaps block which:
   ```
   Credential evaluation → Program admission → Coursework → Exam eligibility → Supervised hours → License
   Visa (F-1) → Program enrollment → OPT → Work authorization → Supervised hours → License
   ```

6. **Prioritized action plan:**

   | Priority | Action | Addresses gap(s) | Start | Duration | Cost |
   |---|---|---|---|---|---|
   | 1 (NOW) | Order transcripts from home university | Documentation | Today | 2-4 weeks | $20-50 |
   | 2 (NOW) | Begin credential evaluation (WES) | Documentation | Today | 6-8 weeks | $200-350 |
   | 3 (SOON) | Research CACREP programs accepting international students | Education | This month | ongoing | $0 |
   | ... | ... | ... | ... | ... | ... |

7. **Update the profile.** Write the gap analysis results to the "Current Gaps" section of the pathway profile.

8. **Offer next steps:**
   > 1. `/legal-pathways:credential-engineering` — deep dive on [highest-priority credential]
   > 2. `/legal-pathways:immigration-pathway` — visa/immigration strategy
   > 3. `/legal-pathways:pathway-comparison` — compare jurisdiction options
   > 4. **Edit profile** — update the pathway profile with new information
