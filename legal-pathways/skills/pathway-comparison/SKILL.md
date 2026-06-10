---
name: pathway-comparison
description: >
  Compare multiple pathway options across jurisdictions with cost-benefit
  analysis. Produces scored comparison matrices for credential, licensing,
  and immigration pathways. The "which route should I take?" skill.
argument-hint: '[pathway A] vs [pathway B] or "compare all options for [target]"'
tools:
  - web_search
categories:
  - comparison
  - analysis
  - planning
version: 0.1.0
---

# /pathway-comparison

Compares multiple pathway options side-by-side, scoring them across cost, time, difficulty, recognition, and strategic value. Helps you decide which route to take when multiple options exist.

## Instructions

1. **Load pathway profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`.

2. **Identify the comparison.** From $ARGUMENTS:
   - **Specific comparison**: "FAA PPL vs SACAA PPL" or "Singapore GIP vs PTS route"
   - **All options for a target**: "compare all options for Singapore citizenship"
   - **Cross-domain**: "get US counselor license vs Singapore PR — which first?"

3. **For each pathway option, assess:**

   | Dimension | Weight | Pathway A | Pathway B | Pathway C |
   |---|---|---|---|---|
   | Total cost | [user priority] | $X | $Y | $Z |
   | Total time | [user priority] | X months | Y months | Z months |
   | Effort/difficulty | [user priority] | Low/Med/High | ... | ... |
   | Success probability | [standard] | X% | Y% | Z% |
   | International recognition | [depends] | Wide/Limited/None | ... | ... |
   | Reversibility | [standard] | Easy/Hard/Irreversible | ... | ... |
   | Opportunity cost | [user priority] | [description] | ... | ... |
   | Strategic value | [depends] | [what it unlocks] | ... | ... |
   | Risk level | [standard] | Low/Med/High | ... | ... |

4. **Produce weighted score:**
   - Assign weights based on user's stated priorities (from profile or $ARGUMENTS)
   - Score each dimension 1-10
   - Calculate weighted total
   - Present ranking with clear rationale

5. **Sensitivity analysis.** Test how the ranking changes if:
   - Budget changes by ±30%
   - Timeline requirement changes
   - A key regulation changes (policy risk)
   - Success probability is lower than estimated

6. **Produce recommendation with rationale:**
   - Clear winner and why
   - When each alternative would be better (conditions for switching)
   - Hybrid strategies (can you pursue multiple in parallel?)

7. **Offer next steps:**
   > 1. **Proceed with [winner]** — I'll produce the detailed SOP
   > 2. **More data on [specific pathway]** — deep dive before deciding
   > 3. **Hybrid strategy** — design a plan that pursues multiple pathways
   > 4. **Revisit assumptions** — change priorities and re-score
