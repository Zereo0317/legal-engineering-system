---
name: cold-start-interview
description: >
  Onboarding interview for Legal Pathways Engineering. Captures your background,
  qualifications, target credentials, budget, timeline, and risk tolerance.
  Populates the pathway profile that all other skills read.
argument-hint: '[--redo to re-run]'
tools: []
categories:
  - onboarding
  - profile
version: 0.1.0
---

# /cold-start-interview

Interviews you to build your Legal Pathways profile. Every other skill in this plugin reads this profile before doing anything — get this right and everything downstream is calibrated.

## Instructions

1. **Check for existing profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`. If it exists and has non-placeholder values, ask if the user wants to update specific sections or start over.

2. **If new or --redo, run the interview.** Ask questions in this order, grouping related questions to avoid excessive back-and-forth:

   ### Round 1: Who are you?
   - Name, age, current nationality/nationalities
   - Current country of residence and tax residence
   - Languages spoken and proficiency levels (with any certifications like TOEFL, IELTS)

   ### Round 2: What do you have?
   - Educational background (every degree, institution, country, field, year, credits)
   - Professional experience (roles, organizations, countries, duration)
   - Any existing professional licenses or certifications
   - Any credential evaluations already completed (WES, ECE, etc.)
   - Any supervised clinical/professional hours logged
   - Current immigration status in relevant countries

   ### Round 3: What do you want?
   - Target credentials (up to 3) — what license, certification, or status?
   - Target jurisdictions — where do you want to be licensed/reside?
   - Why — career goal, visa pathway, personal interest, lifestyle?
   - Budget — total budget per target
   - Timeline — when do you need this by?
   - Risk tolerance — conservative (safest path), moderate, or aggressive (fastest/cheapest)?

   ### Round 4: Constraints and preferences
   - Are you willing to relocate temporarily for education/training?
   - Can you study full-time or must it be part-time/online?
   - Any visa restrictions that limit where you can study/work?
   - Family considerations (spouse, children — affects immigration pathways)?
   - Any existing connections in target jurisdictions (employers, sponsors, family)?

3. **Write the profile.** Copy the template from `legal-pathways/CLAUDE.md` to `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md` and fill in all fields.

4. **Suggest next steps:**
   > **Profile saved.** Here's what I recommend:
   > 1. `/legal-pathways:gap-analysis` — I'll identify every gap between where you are and where you want to be
   > 2. `/legal-pathways:credential-engineering` — deep dive on your professional licensing pathway
   > 3. `/legal-pathways:immigration-pathway` — optimize your immigration strategy
   > 4. `/legal-pathways:aviation-licensing` — design your pilot certification pathway
   > 5. Edit the profile directly — `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`
