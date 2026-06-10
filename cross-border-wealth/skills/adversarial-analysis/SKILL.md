---
name: adversarial-analysis
description: >
  This skill should be used when the user asks to stress-test a legal position,
  evaluate arguments from both sides, assess litigation risk, or run adversarial
  analysis. Spawns advocate, adversary, and judicial-analyst perspectives in
  sequence to produce a balanced assessment with probability-weighted outcomes.
  Can generate an interactive HTML report with three-column layout.
argument-hint: '[legal position | claim | structure to test]'
tools:
  - westlaw_search_cases
  - westlaw_get_case
  - westlaw_search_eu_law
  - westlaw_classic_search
  - web_search
categories:
  - litigation
  - risk
  - analysis
version: 0.1.0
---

# /adversarial-analysis

Stress-tests a legal position by running a structured adversarial process. Three analytical perspectives produce a balanced risk assessment. Optionally generates an interactive HTML report.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Identify the position to test.** Ask the user to articulate:
   - The legal position, claim, or structure under review
   - The jurisdiction(s) involved
   - The counterparty or adversary (regulator, tax authority, opposing counsel, etc.)
   - Any known weaknesses or concerns

3. **Phase 1: Advocate.** Construct the strongest possible case FOR the position:
   - Identify every supporting legal authority (statutes, cases, rulings, guidance)
   - Articulate the policy rationale that supports the position
   - Find analogous situations where similar positions prevailed
   - Anticipate and preemptively rebut likely attacks
   - Assign each argument an ID: `ADV-001`, `ADV-002`, etc.
   - Score each argument's strength: Strong (8-10) / Moderate (5-7) / Weak (1-4)

4. **Phase 2: Adversary.** Construct the strongest possible case AGAINST the position:
   - Identify every authority that undermines the position
   - Find the "parade of horribles" — worst-case interpretations
   - Identify factual vulnerabilities and evidentiary gaps
   - Articulate the policy rationale for denying the position
   - Attack each ADV argument directly where possible
   - Assign each argument an ID: `OPP-001`, `OPP-002`, etc.
   - Score each argument's severity: Critical (8-10) / Significant (5-7) / Minor (1-4)

5. **Phase 3: Judicial Analyst.** Neutral assessment synthesizing both sides:
   - For each ADV/OPP pair, assess which is more persuasive and why
   - Identify the "swing factors" — facts or law that could tip the outcome
   - Assess the decision-maker's likely perspective
   - Consider procedural factors (burden of proof, standard of review, deference)
   - Probability assessment with percentage outcomes

6. **Produce structured output** using the standard text format (argument map table, probability assessment table, decision tree).

7. **Offer rich output.** If the user wants a visual report, generate an interactive HTML report using the template at `${CLAUDE_PLUGIN_ROOT}/assets/adversarial-report.html`:
   - Copy the template to the output location
   - Use Edit to inject content into placeholder zones
   - Three-column layout: Advocate | Judicial Analysis | Adversary
   - Argument cards with strength/severity badges
   - Probability meter visualization
   - Decision tree at bottom

8. **Offer next steps:**
   > 1. **Visual report** — I'll generate an interactive HTML report
   > 2. **Strengthen** — I'll propose modifications to improve the weakest arguments
   > 3. **Research** — I'll find additional authorities on [specific swing factor]
   > 4. **Alternative** — I'll design an alternative approach avoiding key vulnerabilities
   > 5. **Memo** — I'll draft a formal legal memorandum documenting this analysis
   > 6. **Monitor** — I'll identify cases/rulings to watch that could affect this position
