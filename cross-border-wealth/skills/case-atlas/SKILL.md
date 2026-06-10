---
name: case-atlas
description: >
  Interactive Litigation Star Atlas — 15 landmark cross-border wealth and tax
  cases across 8 jurisdictions. Browse, filter, research, and use the built-in
  LLM research prompts. Each case is a fully briefed "system" with facts,
  analysis, reading guide, and verified source links.
argument-hint: '[system number | jurisdiction filter | topic | "all" | "prompt <N>"]'
tools:
  - westlaw_classic_search
  - westlaw_classic_get_document
  - westlaw_search_cases
  - westlaw_get_case
  - westlaw_search_singapore_cases
  - westlaw_get_singapore_judgment
  - web_search
categories:
  - research
  - litigation
version: 0.1.0
---

# /case-atlas

The Litigation Star Atlas: 15 landmark cases that shape modern estate planning, trust governance, transfer pricing, and tax enforcement. A navigable catalog spanning 8 jurisdictions with full briefings, research prompts, and verified source links.

## Instructions

1. **Load the atlas.** Read `${CLAUDE_PLUGIN_ROOT}/references/litigation-star-atlas.md`.

2. **Determine what the user wants.** From $ARGUMENTS:
   - A system number (e.g., "6" or "System 06") → show that case's full panel
   - A jurisdiction filter (e.g., "Singapore" or "EU") → show cases in that jurisdiction
   - A topic (e.g., "transfer pricing" or "trust arbitration") → show relevant cases
   - "all" → show the full atlas index with one-line summaries
   - "prompt N" → extract and present the LLM Research Prompt for System N
   - No argument → show the atlas index and ask what they want to explore

3. **For each case shown, present:**

   **Header:** System number, case name, citation, court, date, jurisdiction tags, topic tags.

   **Four sections:**
   - **01 Briefing** — the facts, the parties, and what was at stake
   - **02 Analysis** — the reasoning and the holding
   - **03 Reading Guide** — what to look for, what to compare it with
   - **04 Sources & Prompts** — verified links + copy-ready research prompts

4. **Verify currency.** For each case shown, run a web search to check:
   - Has this case been appealed, overruled, or distinguished since the atlas was compiled?
   - Are the source links still live?
   - Any new developments?

   Tag the status: `[current as of YYYY-MM-DD]` or `[update found — see note]`.

5. **Connect to the practice profile.** If the practice profile is populated, note which cases are most relevant to the user's jurisdiction footprint and structure types:
   - "System 04 (Credit Suisse v Ivanishvili) is directly relevant — you have Singapore trust structures."
   - "System 06 (Apple state aid) applies to your Irish IP holding arrangement."

6. **Offer next steps:**

   > **What next?**
   > 1. **Deep research** — I'll use Westlaw Classic to pull the full opinion and subsequent treatment for [case]
   > 2. **Apply to your structure** — I'll analyze how [case]'s holding affects your [entity/arrangement]
   > 3. **Find similar cases** — I'll search for cases that cite or distinguish [case]
   > 4. **Run the master prompt** — I'll execute the atlas-wide research prompt across all 15 cases
   > 5. **HTML report** — interactive atlas with filters, expandable panels, and source links
   > 6. **Something else**

## The Atlas Index

| # | Case | Jurisdiction | Topic |
|---|---|---|---|
| 01 | Estate of Warne v. Commissioner | US | Valuation discounts, charitable deduction |
| 02 | Nelson v. Commissioner | US | Tiered discounts, defined-value clause |
| 03 | Carlson v. Colangelo | US (NY) | No-contest clause, in terrorem |
| 04 | Credit Suisse Trust v. Ivanishvili | Singapore | Trustee good faith, fiduciary duty |
| 05 | Commissioner of Taxation v. Bendel | Australia | Family trusts, UPE, Division 7A |
| 06 | Commission v. Ireland and Apple | EU | State aid, €13bn recovery |
| 07 | Starbucks UK | UK | Transfer pricing, social licence |
| 08 | Rio Tinto — ATO Settlement | Australia | Marketing hub, transfer pricing |
| 09 | HMRC v. BlackRock Holdco 5 | UK | Intra-group debt, unallowable purpose |
| 10 | Belgian Assoc. of Tax Lawyers v. EU | EU | DAC6 validity, legal privilege |
| 11 | Zhong Shan v. RG Strategy Fund VCC | Singapore | VCC sub-fund liquidation |
| 12 | Pinnacle Trust v. McTaggart | US (MS) | Trustee duty, arbitration |
| 13 | McArthur v. McArthur | US (CA) | Trust arbitration clause |
| 14 | DNQ v. DNR | Singapore | Litigation funding |
| 15 | AI Citation Sanctions | Multi | Hallucinated citations, sanctions |
