---
name: case-research
description: >
  Deep legal research using Westlaw Classic, CourtListener, EUR-Lex, and web
  search. Find cases, statutes, regulations, and treaties on any cross-border
  wealth or tax topic. Produces a sourced research memo with citations verified
  against primary sources.
argument-hint: '[research question | case citation | statute | treaty article | topic]'
tools:
  - westlaw_classic_search
  - westlaw_classic_get_document
  - westlaw_search_cases
  - westlaw_get_case
  - westlaw_search_legislation
  - westlaw_search_regulations
  - westlaw_get_cfr_section
  - westlaw_search_eu_law
  - westlaw_unified_search
  - westlaw_health_check
  - web_search
categories:
  - research
  - litigation
version: 0.1.0
---

# /case-research

Deep legal research across multiple databases. Routes queries to the right tool, verifies citations against primary sources, and produces a research memo with full attribution.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` for jurisdiction footprint and risk posture context.

2. **Understand the query.** From $ARGUMENTS, determine:
   - Is this a specific case lookup? (citation or case name provided)
   - Is this a statute/regulation lookup? (section number or statute name provided)
   - Is this a treaty question? (treaty pair or article mentioned)
   - Is this a topical research question? (e.g., "what's the current position on substance requirements in Cayman?")

3. **Pre-flight check.** Test whether Westlaw Classic is responding. Record the result for the reviewer note.

4. **Route to tools.** Use the optimal tool for each query type:

   | Query Type | Primary Tool | Fallback |
   |---|---|---|
   | US case law (search) | `westlaw_search_cases` | `westlaw_classic_search` → web search |
   | US case law (full opinion) | `westlaw_get_case` | `westlaw_classic_get_document` |
   | US legislation/bills | `westlaw_search_legislation` | web search (congress.gov) |
   | US regulations | `westlaw_search_regulations` | web search (federalregister.gov) |
   | CFR section | `westlaw_get_cfr_section` | web search (ecfr.gov) |
   | EU law | `westlaw_search_eu_law` | web search (eur-lex.europa.eu) |
   | International/comparative | `westlaw_classic_search` | web search |
   | Multi-jurisdiction | `westlaw_unified_search` | parallel web searches |
   | Tax treaties | web search (tax treaty databases) | model knowledge with flag |
   | Non-US case law | `westlaw_classic_search` | web search (jurisdiction-specific databases) |

5. **For each source found:**
   - Record the full citation (case name, court, date, reporter)
   - Verify the citation against the primary source (is this the actual holding, not dicta, not a dissent, not a quoted argument the court rejected?)
   - Check subsequent treatment (has it been appealed, overruled, distinguished, followed?)
   - Tag with provenance (`[Westlaw]`, `[CourtListener]`, `[EUR-Lex]`, `[web search — verify]`, `[model knowledge — verify]`)

6. **Produce the research memo.** Structure:

   **Question presented:** [the research question, precisely stated]

   **Short answer:** [2-3 sentences — the bottom line]

   **Analysis:** [structured by issue, with citations. Each legal proposition has a source tag. Jurisdiction-specific throughout.]

   **Key authorities:**
   | Authority | Citation | Jurisdiction | Holding | Status | Source |
   |---|---|---|---|---|---|
   | [case/statute] | [citation] | [jurisdiction] | [one-line holding] | [current/overruled/under appeal] | [provenance tag] |

   **Open questions:** [what remains unresolved, what needs further research, what the user should verify]

7. **Cross-reference with the Star Atlas.** If any of the 15 atlas cases are relevant to the research question, note the connection and suggest reviewing the atlas entry.

8. **Offer next steps:**

   > **What next?**
   > 1. **Go deeper** — I'll pull the full opinion(s) and analyze the reasoning in detail
   > 2. **Apply to your structure** — I'll apply these findings to [entity/arrangement from practice profile]
   > 3. **Find contrary authority** — I'll search for cases that reach the opposite conclusion
   > 4. **HTML report** — formatted research memo with linked citations
   > 5. **Send to team** — I'll draft a Slack message or email summarizing the findings
   > 6. **Something else**

## Verification Protocol

- Every citation is verified against at least one primary or authoritative secondary source
- If Westlaw Classic is connected, the `[Westlaw]` tag requires the citation to appear in a Westlaw result
- Model knowledge citations are ALWAYS tagged `[model knowledge — verify]`
- The reviewer note lists: tools connected, queries run, results found, verification status
- If a citation cannot be verified, it is flagged: "Could not verify — treat as unconfirmed"
