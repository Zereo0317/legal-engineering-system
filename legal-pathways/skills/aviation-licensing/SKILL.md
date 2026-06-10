---
name: aviation-licensing
description: >
  Compare aviation authorities and design the fastest, cheapest path to pilot
  certification. Covers PPL, instrument rating, multi-engine rating, type
  ratings for jets, and international license conversion. The "how do I fly
  a private jet with minimum effort?" skill.
argument-hint: '[target: PPL | CPL | type rating | "fly private jets"] [jurisdiction or "cheapest" or "fastest"]'
tools:
  - westlaw_search_regulations
  - westlaw_get_cfr_section
  - web_search
categories:
  - aviation
  - licensing
  - regulatory-arbitrage
version: 0.1.0
---

# /aviation-licensing

Designs the optimal pathway to pilot certification, treating aviation authorities (FAA, EASA, SACAA, CAAS, CAAC, DGCA) as modular regulatory systems. Each authority has different hour requirements, exam difficulty, cost, and international recognition.

## Instructions

1. **Load pathway profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`.

2. **Clarify the target.** From $ARGUMENTS:
   - **End goal**: What do you want to do? (Fly a private jet? Fly recreationally? Career pilot?)
   - **Aircraft type**: Specific aircraft in mind? (Citation, Phenom, G650, "any light jet")
   - **Jurisdiction**: Where do you want to fly? (US, Europe, Asia, "anywhere")
   - **Optimization**: Fastest? Cheapest? Least training time? Most internationally portable?

   If the user says "private jet" or "fly a jet," clarify:
   - A PPL (Private Pilot License) alone does NOT let you fly a jet
   - Flying a private jet requires: PPL + Instrument Rating + Multi-Engine Rating + Type Rating
   - The minimal path depends heavily on the specific aircraft

3. **Load reference data.** Read `legal-pathways/references/aviation-licensing-global.md`. Verify current data via web search.

4. **Map the complete certification stack:**

   ### Level 1: Private Pilot License (PPL)
   For each candidate jurisdiction:
   | Authority | Min hours | Solo hours | Cross-country | Night | Exam | Medical | Cost | Timeline |
   |---|---|---|---|---|---|---|---|---|
   | FAA (US) | 40 hrs | 10 hrs | 5 hrs (150nm) | 3 hrs | Written + checkride | Class 3 | $12K-18K | 2-6 months |
   | EASA (EU) | 45 hrs | 10 hrs | 5 hrs (150nm) | Required | Written + skill test | Class 2 | $15K-25K | 3-8 months |
   | SACAA (ZA) | 45 hrs | ... | ... | ... | ... | ... | $8K-12K | 3-6 months |
   | CAAS (SG) | 45 hrs | ... | ... | ... | ... | ... | $18K-30K | 4-8 months |
   | CAAC (CN) | 40 hrs | ... | ... | ... | ... | ... | $15K-25K | 3-6 months |
   | DGCA (IN) | 40 hrs | ... | ... | ... | ... | ... | $6K-10K | 3-6 months |
   | CAA Philippines | 40 hrs | ... | ... | ... | ... | ... | $5K-7K | 3-6 months |

   ### Level 2: Instrument Rating (IR)
   - Required to fly in clouds/poor visibility and most jet operations
   - FAA: 50 hrs cross-country PIC + 40 hrs instrument time + written + checkride
   - Adds $10K-20K and 2-4 months

   ### Level 3: Multi-Engine Rating (ME)
   - Required for any multi-engine aircraft (all jets)
   - FAA: No minimum hours (typically 10-15 hrs training) + checkride
   - Adds $5K-10K and 1-2 weeks

   ### Level 4: Type Rating
   - Required for aircraft >12,500 lbs MTOW or any turbojet
   - Aircraft-specific (e.g., CE-525 for Citation CJ series)
   - Typically 10-14 days ground school + simulator + checkride
   - Adds $15K-45K per type

5. **Accelerated program analysis.** Research and present accelerated options:
   - Part 141 accelerated PPL programs (14-21 days intensive)
   - Combined PPL+IR+ME programs
   - "Zero to jet" programs (exist at some flight schools)
   - Simulator-heavy programs that minimize actual flight hours

6. **International license conversion analysis:**
   - ICAO license conversion pathways between authorities
   - Which authorities have mutual recognition agreements?
   - Converting a foreign PPL to FAA (14 CFR § 61.75 — foreign license validation)
   - Converting FAA to EASA, CAAS, etc.

7. **Jurisdiction shopping matrix.** Rank jurisdictions by optimization target:

   | Rank | Jurisdiction | Total cost | Total time | Recognition | Weather factor | Language |
   |---|---|---|---|---|---|---|
   | 1 | [Best for user's optimization target] | ... | ... | ... | ... | ... |

   Factors:
   - **Cost**: Training + living expenses + medical + exam fees
   - **Time**: Weather days (flyable days per year), instructor availability
   - **Recognition**: How easily does this license convert to other jurisdictions?
   - **Weather**: Year-round flying (South Africa, Philippines, Arizona) vs. seasonal
   - **Language**: Is English instruction available? (Required for international ops)

8. **Produce the SOP:**

   | Step | Action | Timeline | Cost | Prerequisites | CTA |
   |---|---|---|---|---|---|
   | 1 | Medical certificate | Week 1 | $100-300 | None | Book AME appointment |
   | 2 | PPL ground school | Weeks 1-4 | $200-500 | None | Enroll in online ground school |
   | 3 | PPL flight training | Weeks 2-12 | $8K-15K | Medical | Book discovery flight |
   | ... | ... | ... | ... | ... | ... |

9. **"Minimum effort" analysis.** If the user wants the absolute minimum training:
   - Identify aircraft that DON'T require type ratings (under 12,500 lbs, non-turbojet)
   - Light sport aircraft (LSA) option — even fewer hours required
   - Fractional ownership or charter vs. obtaining a license
   - Hiring a pilot (cost-benefit vs. getting licensed yourself)

10. **Offer next steps:**
    > **What next?**
    > 1. **Flight school comparison** — I'll compare specific schools for your chosen jurisdiction
    > 2. **Type rating deep dive** — requirements for [specific aircraft]
    > 3. **License conversion pathway** — how to make your license work in multiple jurisdictions
    > 4. **Cost-benefit: license vs. charter** — is it worth getting the license?
    > 5. **Regulatory research** — I'll pull the actual FARs/regulations for your pathway
    > 6. **Something else**

## Verification

Aviation regulations are verified via web search and, for US regulations, via eCFR (14 CFR Part 61, 91, 135, 142). Requirements change less frequently than tax law but medical standards and training requirements are updated periodically. International requirements are verified against the relevant CAA's official publications.
