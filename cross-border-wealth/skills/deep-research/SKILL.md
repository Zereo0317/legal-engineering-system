---
name: deep-research
description: >
  Deep multilingual legal research across any jurisdiction, culture, and language.
  Searches academic papers, expert commentary, law firm publications, government
  gazettes, regulatory announcements, court decisions, and specialist articles.
  Reads sources in their original language (EN, ZH, JA, KO, FR, DE, ES, AR, PT, IT).
  Use when asked to "research [topic]", "find expert opinions on", "what do scholars say about",
  "find papers on", "research in [language]", or any deep research request.
argument-hint: '"[legal topic]" or "[topic] in [jurisdiction]" or "[topic] in [language]"'
tools:
  - westlaw_unified_search
  - westlaw_classic_search
  - westlaw_search_cases
  - westlaw_search_eu_law
  - westlaw_search_taiwan_judgments
  - westlaw_search_singapore_cases
  - westlaw_eu_compliance_search
  - westlaw_oecd_get_treaty
  - westlaw_search_sec_filings
  - web_search
  - web_fetch
categories:
  - research
  - multilingual
  - academic
version: 0.1.0
---

# /deep-research

Conducts deep, multilingual legal research across jurisdictions. Finds and synthesizes primary sources, academic scholarship, expert commentary, and practitioner analysis — reading sources in their original language when the user's cultural or linguistic context requires it.

## Instructions

1. **Understand the research question.** From $ARGUMENTS:
   - What legal topic or question?
   - Which jurisdiction(s)?
   - What language(s) should sources be in? (Default: user's language preferences from CLAUDE.md profile, plus English)
   - What type of sources? (case law, legislation, academic papers, expert commentary, all)
   - Depth: quick survey (5-10 sources) or exhaustive (20+ sources)?

2. **Multi-source research strategy.** Execute searches in parallel across source tiers:

   ### Tier 1: Primary Legal Sources (via MCP tools)
   - **Case law**: westlaw_unified_search, westlaw_search_cases, westlaw_classic_search
   - **Legislation**: westlaw_search_legislation, westlaw_get_cfr_section
   - **EU law**: westlaw_search_eu_law, westlaw_eu_compliance_search
   - **Taiwan law**: westlaw_search_taiwan_judgments, westlaw_get_taiwan_statute
   - **Singapore law**: westlaw_search_singapore_cases
   - **OECD treaties**: westlaw_oecd_get_treaty, westlaw_oecd_model_convention
   - **SEC filings**: westlaw_search_sec_filings, westlaw_sec_full_text_search

   ### Tier 2: Academic & Expert Sources (via web search + fetch)
   - **Academic papers**: Search SSRN, Google Scholar, arXiv (for AI governance), JSTOR
   - **Law reviews**: Search HeinOnline, Westlaw secondary sources, university law reviews
   - **Expert commentary**: Search law firm publications (Baker McKenzie, Linklaters, Deloitte Tax, PwC, EY, KPMG), think tanks (OECD, IMF, World Bank, Brookings, Tax Foundation)
   - **Government sources**: Official gazettes, tax authority guidance, regulatory announcements
   - **News**: Legal news (Law360, Reuters Legal, Bloomberg Law, The Law Society Gazette)

   ### Tier 3: Multilingual & Culture-Specific Sources
   - **Chinese (ZH)**: Search in Simplified and Traditional Chinese
     - 法源法律網 (lawbank.com.tw) — Taiwan case law and legislation
     - 中國裁判文書網 — PRC court decisions
     - 月旦法學知識庫 — Taiwan legal journals
     - 元照出版 — Legal commentary
   - **Japanese (JA)**: 裁判所 (courts.go.jp), 法令データ提供システム (e-Gov)
   - **Korean (KO)**: 법제처 국가법령정보센터 (law.go.kr)
   - **French (FR)**: Legifrance, EUR-Lex (FR), Dalloz
   - **German (DE)**: Beck-Online, EUR-Lex (DE), Bundesgesetzblatt
   - **Spanish (ES)**: BOE (boe.es), Tirant lo Blanch
   - **Arabic (AR)**: Regional regulatory authority websites
   - **Portuguese (PT)**: DRE (dre.pt), Planalto (planalto.gov.br)

3. **For each source found, extract and record:**

   | Field | Content |
   |---|---|
   | **Title** | Full title in original language + English translation |
   | **Author** | Author name, affiliation, credentials |
   | **Source** | Journal, court, publication, or website |
   | **Date** | Publication or decision date |
   | **Language** | Original language of the source |
   | **Key findings** | 2-3 sentence summary of the relevant argument or holding |
   | **Provenance** | `[Westlaw]`, `[web search]`, `[web fetch — verify]`, `[model knowledge — verify]` |
   | **URL** | Direct link to the source where available |

4. **Synthesize findings into a research memo:**

   ### Executive Summary
   One paragraph answering the research question with the weight of authority.

   ### Consensus View
   What do most experts/authorities agree on? With citations.

   ### Dissenting / Minority Views
   Where do experts disagree? What are the strongest counter-arguments?

   ### Jurisdiction-Specific Positions
   How does each relevant jurisdiction treat this issue? Note where law diverges.

   ### Cultural Context
   How do different legal cultures approach this issue? (e.g., common law adversarial vs civil law inquisitorial; Confucian family law vs Western individual rights; Islamic finance vs conventional)

   ### Evolving Trends
   What is changing? Recent legislative proposals, pending cases, OECD recommendations, enforcement trends.

   ### Knowledge Gaps
   What we could not find or verify. What would require deeper research (e.g., access to paywalled databases, local practitioner interviews).

5. **Source quality assessment:**

   | Quality Tier | Examples | Weight |
   |---|---|---|
   | **Authoritative** | Court decisions, enacted legislation, official guidance | Highest |
   | **Expert** | Law firm memoranda, Big Four publications, OECD reports | High |
   | **Academic** | Peer-reviewed papers, law review articles | High |
   | **Practitioner** | Blog posts, conference papers, CLE materials | Medium |
   | **Commentary** | News articles, opinion pieces, social media | Low (context only) |

6. **Language handling rules:**
   - Always search in the **original language** of the jurisdiction being researched
   - Present key findings **bilingually** (original language + user's preferred language)
   - For legal terms that don't translate cleanly, provide the original term with an explanatory gloss (e.g., 善良管理人之注意 — duty of care of a good administrator)
   - Flag **false friends** — terms that look similar across legal systems but have different meanings (e.g., "consideration" in common law vs "causa" in civil law)

7. **Offer next steps:**
   > **What next?**
   > 1. **Deep dive** — full analysis on a specific sub-topic or case
   > 2. **Adversarial test** — stress-test a position found in the research
   > 3. **Comparative analysis** — systematic comparison across jurisdictions
   > 4. **Expert opinion draft** — draft a memo or opinion letter based on findings
   > 5. **Translate key sources** — full legal translation of critical documents
   > 6. **Monitor this topic** — set up regulatory monitoring for changes
   > 7. **Something else**

## Verification

All sources are tagged with provenance. Primary legal sources are verified against MCP tools (Westlaw, CourtListener, EUR-Lex, Taiwan Judicial Yuan). Academic and expert sources are verified via web fetch where URLs are available. Model knowledge is explicitly tagged as `[model knowledge — verify]` and never presented as authoritative.
