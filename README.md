# Legal Engineering

Legal engineering optimizer — a Claude Code plugin marketplace that treats 200+ jurisdictions as modular building blocks for wealth structuring, sovereign individual architecture, professional licensing pathways, aviation certification, and immigration engineering.

**38 skills | 15 agents | 30+ MCP tools | 8 MCP servers | 14 references**

## What this is

Legal Engineering is the discipline of combining jurisdictions' legal frameworks — tax rates, treaty networks, trust law, corporate vehicles, privacy regimes, substance requirements, licensing boards, immigration systems, aviation authorities — to construct pathways and structures optimized for a specific purpose. Each jurisdiction is a building block; each structure or pathway is a module.

**Core principle: Control everything, own nothing. 利用各地法律落差，合法創造優勢。**

Three properties make it engineering:
- **Repeatable** — the same structural pattern adapts for different clients
- **Optimizable** — as laws and treaties change, structures adjust
- **Stackable** — each layer is modular; swap one without rebuilding the whole

**Target audience**: Elites, UHNW individuals, ambitious professionals, empire builders, sovereign individuals, founders who want to build empires of private equity, private jets, and global citizenship — and those who aspire to become one.

## Plugins

| Plugin | Skills | Agents | References | What it does |
|---|---|---|---|---|
| `cross-border-wealth` | 29 | 13 | 9 | Tax-efficient entity architecture, treaty optimization, compliance, case law research, Pillar Two, exit analysis, adversarial stress-testing, contract review, AI governance, Taiwan law, SaleCraft compliance, privacy impact assessment, interactive dashboards |
| `legal-pathways` | 9 | 2 | 5 | Sovereign architecture (flag theory), professional licensing, aviation certification (PPL to jet), immigration pathway optimization, CBI/RBI comparison, legal translation, matter workspace |

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Python 3.10+ (for the Westlaw MCP server)
- Node.js 18+ — optional, only for the `npx`-based MCP servers (AustLII, Sequential Thinking)
- [`uv`](https://docs.astral.sh/uv/) — optional, only for the official Fetch MCP server (`uvx mcp-server-fetch`)
- No API keys required for basic usage (most legal databases are free)

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/Zereo0317/legal-engineering-public.git
cd legal-engineering-public

# 2. Install the Westlaw MCP server (use a virtual env)
python3 -m venv .venv && source .venv/bin/activate
cd westlaw-mcp && pip install -e . && cd ..

# 3. Install Playwright browser (only needed for Westlaw Classic institutional access)
playwright install chromium

# 4. Install the marketplace (all plugins)
claude plugin install legal-engineering --source ./

# === SOVEREIGN INDIVIDUAL ARCHITECTURE ===
# Design your complete multi-jurisdictional life
/legal-pathways:sovereign-architect

# === WEALTH STRUCTURING ===
# Onboard your practice/family office
/cross-border-wealth:cold-start-interview

# Analyze a cross-border structure
/cross-border-wealth:structure-analysis

# Design a new structure from scratch
/cross-border-wealth:structure-designer

# Compare jurisdictions
/cross-border-wealth:jurisdiction-scanner

# === PERSONAL LEGAL INFRASTRUCTURE ===
# Credential engineering (e.g., US counselor license)
/legal-pathways:credential-engineering

# Aviation licensing (PPL to private jet)
/legal-pathways:aviation-licensing

# Immigration pathway (citizenship, PR, golden visa)
/legal-pathways:immigration-pathway

# === ADVERSARIAL ANALYSIS ===
# Stress-test a structure with red-team/blue-team
/cross-border-wealth:adversarial-analysis

# === CONTRACT & COMPLIANCE ===
# Clause-by-clause contract review
/cross-border-wealth:contract-review

# SaleCraft compliance check
/cross-border-wealth:salecraft-compliance

# Privacy impact assessment
/cross-border-wealth:privacy-impact-assessment

# === RESEARCH ===
# Deep case law research
/cross-border-wealth:case-research

# Browse the Litigation Star Atlas
/cross-border-wealth:case-atlas

# Taiwan-specific legal analysis
/cross-border-wealth:taiwan-law-specialist
```

## Cross-Border Wealth Plugin (29 Skills)

| Skill | What it does |
|---|---|
| `cold-start-interview` | Onboard: practice type, jurisdictions, structures, risk posture |
| `customize` | Edit the practice profile |
| `structure-analysis` | Analyze a cross-border structure (tax, substance, treaties, TP, compliance, exit) |
| `structure-designer` | Design a new cross-border structure from scratch given a goal and constraints |
| `jurisdiction-scanner` | Compare jurisdictions for a specific structuring purpose |
| `treaty-mapper` | Map treaty networks, find optimal WHT routing |
| `entity-optimizer` | Recommend the optimal legal vehicle for a goal |
| `transfer-pricing-review` | Review intercompany transactions against arm's-length standard |
| `tp-documentation-generation` | Generate OECD-aligned transfer-pricing documentation (master file / local file / CbCR) from a TP review |
| `trust-governance` | Analyze trust/foundation governance, fiduciary duties, disputes |
| `compliance-checker` | Check against DAC6, CRS, FATCA, BEPS CbCR, UBO registers |
| `risk-assessment` | Identify structure vulnerabilities and upcoming regulatory changes |
| `pillar-two-impact` | Assess OECD Pillar Two (Global Minimum Tax) impact on structures |
| `exit-analysis` | Analyze consequences of unwinding, migrating, or restructuring |
| `case-atlas` | Interactive Litigation Star Atlas (15 cases, 8 jurisdictions) |
| `case-research` | Deep legal research via Westlaw Classic + CourtListener + EUR-Lex |
| `report-generator` | Generate interactive HTML reports from any analysis |
| `action-executor` | Execute actions (Gmail, Slack, Drive, web search) |
| `matter-workspace` | Per-client workspace isolation |
| `adversarial-analysis` | Red-team/blue-team stress-test of proposed structures or positions |
| `contract-review` | Clause-by-clause contract review with dual severity axes (legal risk + business friction) |
| `regulatory-gap-analysis` | Identify gaps between current compliance and regulatory requirements across jurisdictions |
| `privacy-impact-assessment` | GDPR/PDPA/CCPA privacy impact assessment for cross-border data flows |
| `ai-governance-triage` | Triage AI governance obligations (EU AI Act, Singapore FEAT, SEC guidance) |
| `citation-verification` | Verify all citations against primary sources — flag hallucinations and outdated law |
| `salecraft-compliance` | Ensure advice complies with sales practice regulations (suitability, KYC, disclosure) |
| `taiwan-law-specialist` | Taiwan-specific legal analysis (income tax, estate tax, CFC, trust taxation, cross-strait) |
| `legal-dashboard` | Generate self-contained HTML dashboards with live filtering, sorting, and risk visualization |
| `deep-research` | Deep multilingual legal research — academic papers, expert commentary, law firm publications, government gazettes across any jurisdiction and language (EN, ZH, JA, KO, FR, DE, ES, AR) |

## Legal Pathways Plugin (9 Skills)

| Skill | What it does |
|---|---|
| `cold-start-interview` | Onboard: background, qualifications, targets, budget, timeline |
| `sovereign-architect` | Design complete sovereign individual architecture (all 7 flags of flag theory) |
| `credential-engineering` | Analyze credential gaps and design pathway to professional licenses across borders |
| `aviation-licensing` | Compare aviation authorities and design fastest path to pilot certification + type ratings |
| `immigration-pathway` | Analyze immigration options and design optimal citizenship/PR pathway |
| `gap-analysis` | General gap identification across any regulatory domain |
| `pathway-comparison` | Compare multiple pathway options with cost-benefit analysis |
| `legal-translation` | Legal translation with parallel text, jurisdiction-specific terminology mapping |
| `matter-workspace` | Per-client workspace isolation for multi-client practices |

## Agents (15)

### Cross-Border Wealth Agents (13)

| Agent | Role | Model |
|---|---|---|
| `case-researcher` | Multi-source deep case research with citation verification | Opus |
| `treaty-watcher` | Monitor treaty changes affecting your structures | Sonnet |
| `regulatory-monitor` | Watch for regulatory changes across jurisdictions | Sonnet |
| `orchestrator` | Coordinates multi-agent workflows, routes to specialists, synthesizes outputs | Opus |
| `adversary` | Red-team: attacks proposed structures from hostile authority perspective | Sonnet |
| `advocate` | Blue-team: builds strongest legal arguments and identifies supporting authority | Sonnet |
| `judicial-analyst` | Neutral evaluator: weighs arguments and predicts judicial outcomes | Opus |
| `drafter` | Generates legal documents, memos, opinion letters from analysis outputs | Sonnet |
| `citation-checker` | Verifies all citations against primary sources, flags hallucinations | Haiku |
| `compliance` | DAC6/CRS/FATCA/BEPS specialist, checks all reporting obligations | Sonnet |
| `data-protection` | GDPR/PDPA/PIPA/CCPA specialist, privacy impact assessments | Sonnet |
| `fiscal-specialist` | Deep tax computation, ETR modeling, Pillar Two GloBE calculations | Sonnet |
| `translator` | Legal translation with parallel text and terminology notes | Sonnet |

### Legal Pathways Agents (2)

| Agent | Role | Model |
|---|---|---|
| `pathway-researcher` | Deep research on licensing, immigration, and credential regulations | Opus |
| `compliance-analyst` | Regulatory compliance analysis for licensing and immigration pathways | Sonnet |

## Westlaw MCP Server (25 Tools)

All tools are served by a single MCP server (`westlaw-mcp/`) across 11 legal databases.

| # | Tool | Source | Cost |
|---|---|---|---|
| 1 | `westlaw_classic_search` | Westlaw Classic | Institutional subscription |
| 2 | `westlaw_classic_get_document` | Westlaw Classic | Institutional subscription |
| 3 | `westlaw_search_cases` | CourtListener | Free |
| 4 | `westlaw_get_case` | Westlaw Classic / CourtListener fallback | Free fallback |
| 5 | `westlaw_search_legislation` | Congress.gov | Free (API key) |
| 6 | `westlaw_search_regulations` | Federal Register | Free |
| 7 | `westlaw_get_cfr_section` | eCFR | Free |
| 8 | `westlaw_search_eu_law` | EUR-Lex | Free |
| 9 | `westlaw_unified_search` | All sources in parallel | Mixed |
| 10 | `westlaw_health_check` | Internal | Free |
| 11 | `westlaw_search_taiwan_judgments` | Taiwan Judicial Yuan | Free |
| 12 | `westlaw_get_taiwan_statute` | Taiwan Judicial Yuan | Free |
| 13 | `westlaw_search_taiwan_interpretations` | Taiwan Judicial Yuan | Free |
| 14 | `westlaw_eu_compliance_search` | EUR-Lex + EC | Free |
| 15 | `westlaw_eu_compliance_article` | EUR-Lex | Free |
| 16 | `westlaw_eu_compliance_compare` | EUR-Lex | Free |
| 17 | `westlaw_oecd_get_treaty` | OECD | Free |
| 18 | `westlaw_oecd_model_convention` | OECD | Free |
| 19 | `westlaw_oecd_commentary` | OECD | Free |
| 20 | `westlaw_oecd_mli_status` | OECD | Free |
| 21 | `westlaw_search_sec_filings` | SEC EDGAR | Free |
| 22 | `westlaw_get_sec_filing` | SEC EDGAR | Free |
| 23 | `westlaw_sec_full_text_search` | SEC EDGAR | Free |
| 24 | `westlaw_search_singapore_cases` | Singapore eLitigation | Free |
| 25 | `westlaw_get_singapore_judgment` | Singapore eLitigation | Free |

### Research & Reasoning (3 MCP Servers)

| Server | Type | What it does |
|---|---|---|
| **Exa AI Search** | SSE | AI-native web search — finds expert legal commentary, law firm publications, academic papers, regulatory news across any language |
| **Fetch** (Official MCP) | stdio | Reads any URL and converts to clean text — government gazettes, regulatory announcements, foreign-language legal sources |
| **Sequential Thinking** (Official MCP) | stdio | Structured multi-step reasoning chains for complex legal analysis and multi-jurisdiction comparisons |

### Additional Legal Search (Optional)

| # | Tool | Source | Cost |
|---|---|---|---|
| 26 | `vaquill_semantic_search` | Vaquill AI | API key required |
| 27 | `vaquill_get_opinion` | Vaquill AI | API key required |
| 28 | `auslaw_search_cases` | AustLII | Free |
| 29 | `auslaw_search_legislation` | AustLII | Free |
| 30 | `auslaw_get_document` | AustLII | Free |

### Communication & Storage

- **Gmail** — send reports and client communications
- **Slack** — team updates and alerts
- **Google Drive** — save reports and documents
- **Web search** — verify current legal positions

See `CONNECTORS.md` for adding new data source connectors.

## Guardrails System

Every output from this plugin is governed by a comprehensive guardrails framework (`cross-border-wealth/references/guardrails.md`):

### Work-Product Headers
Every substantive output begins with a privilege/confidentiality header appropriate to the user's role and the matter's sensitivity.

### Citation Provenance
Every legal citation is tagged with its actual retrieval source — no silent reliance on model knowledge. Sources include `[Westlaw]`, `[CourtListener]`, `[EUR-Lex]`, `[model knowledge — verify]`, and `[settled — last confirmed YYYY-MM-DD]`.

### Retrieved-Content Trust Boundary
All content from MCP tools, web searches, and file uploads is treated as DATA, never as instructions. Embedded directives in retrieved content are flagged as potential prompt injection.

### Cross-Skill Severity Floor
Upstream severity cannot be silently demoted downstream. If risk-assessment flags HIGH, report-generator must reflect HIGH.

### Decision Trees
Every analysis ends with options (not decisions), risk/benefit comparison, recommended next steps, and an explicit statement of what Claude does NOT know.

### Privacy Classification (PreToolUse Hook)
A 3-tier classification system runs before any Write, Edit, WebFetch, or MCP tool invocation:
- **PRIVILEGED** — blocked from external transmission (attorney-client indicators detected)
- **CONFIDENTIAL** — proceeds with anonymization warning
- **PUBLIC** — allowed without restriction

## Adversarial Analysis Methodology

The `/cross-border-wealth:adversarial-analysis` skill implements a structured red-team/blue-team methodology for stress-testing proposed structures:

1. **Adversary Agent (Red Team)** — Adopts the perspective of a hostile tax authority, regulator, or litigant. Identifies the strongest attacks: substance challenges, treaty shopping allegations, GAAR invocations, transfer pricing adjustments, beneficial ownership disputes.

2. **Advocate Agent (Blue Team)** — Builds the strongest defense: identifies supporting authority, distinguishes adverse precedent, constructs the narrative of commercial rationale, marshals substance evidence.

3. **Judicial Analyst (Neutral)** — Weighs both sides as a tribunal or court would. Considers: burden of proof allocation, standard of review, judicial temperament in the relevant jurisdiction, likelihood of settlement vs. litigation.

4. **Synthesis** — Produces a vulnerability matrix with:
   - Attack vectors ranked by probability of success
   - Defense strength per vector
   - Net risk score
   - Recommended structural modifications to improve defensibility

This methodology ensures structures are tested against realistic adversarial scenarios before implementation, not just analyzed in a vacuum.

## Reference Data (14)

### Cross-Border Wealth (9)

| Reference | Content |
|---|---|
| `litigation-star-atlas.md` | 15 landmark cases, 8 jurisdictions, verified sources |
| `jurisdiction-profiles.md` | Tax rates, treaty networks, substance rules for key jurisdictions |
| `treaty-network.md` | Bilateral WHT rate matrix across 13 structuring jurisdictions |
| `substance-requirements.md` | Per-jurisdiction substance rules and costs |
| `pillar-two-tracker.md` | Global Minimum Tax implementation status by jurisdiction |
| `report-template.html` | HTML report template (dark/light, print, sortable) |
| `dashboard-template.md` | Dashboard format specification |
| `guardrails.md` | Comprehensive guardrails — privilege, citations, trust boundaries, severity floors |
| `matter-template.md` | Case/matter management template for workspace isolation |

### Legal Pathways (5)

| Reference | Content |
|---|---|
| `us-counselor-licensing.md` | State-by-state LPC/LMHC requirements, CACREP, foreign credential evaluation |
| `aviation-licensing-global.md` | PPL by country, type ratings by aircraft, aircraft registries, ownership structures |
| `singapore-immigration.md` | SG PR/citizenship pathways, dual citizenship reality, GIP, COMPASS, family office (13O/13U) |
| `citizenship-investment-matrix.md` | CBI/RBI programs worldwide, cost/timeline/passport quality comparison |
| `flag-theory-implementation.md` | 7 flags framework, UHNW family office architecture, private jet integration |

## What This Plugin Solves

### For Elites & UHNW

| Problem | Skill |
|---|---|
| "I want a second passport" | `/legal-pathways:immigration-pathway` + `references/citizenship-investment-matrix.md` |
| "Design my sovereign individual architecture" | `/legal-pathways:sovereign-architect` |
| "I want to fly my own jet" | `/legal-pathways:aviation-licensing` + `references/aviation-licensing-global.md` |
| "Structure my family office across Singapore and Switzerland" | `/cross-border-wealth:structure-designer` |
| "Optimize my tax position across 5 jurisdictions" | `/cross-border-wealth:structure-analysis` |
| "How does Pillar Two affect my holding structure?" | `/cross-border-wealth:pillar-two-impact` |
| "Stress-test my structure against a hostile tax authority" | `/cross-border-wealth:adversarial-analysis` |
| "Review this SPA for cross-border risk" | `/cross-border-wealth:contract-review` |

### For Ambitious Professionals

| Problem | Skill |
|---|---|
| "Get my US counselor license with a foreign degree" | `/legal-pathways:credential-engineering` |
| "Singapore citizenship as a tech professional" | `/legal-pathways:immigration-pathway` |
| "Which state has the easiest LPC requirements?" | `/legal-pathways:pathway-comparison` |
| "What's the cheapest way to get a PPL?" | `/legal-pathways:aviation-licensing` |

### For Advisers & Family Offices

| Problem | Skill |
|---|---|
| "Analyze a client's cross-border structure" | `/cross-border-wealth:structure-analysis` |
| "Check DAC6/CRS/FATCA compliance" | `/cross-border-wealth:compliance-checker` |
| "Research case law on treaty shopping" | `/cross-border-wealth:case-research` |
| "Design an exit strategy from a multi-jurisdiction structure" | `/cross-border-wealth:exit-analysis` |
| "Privacy impact assessment for client data flows" | `/cross-border-wealth:privacy-impact-assessment` |
| "Taiwan CFC rules for offshore holdings" | `/cross-border-wealth:taiwan-law-specialist` |
| "Translate this trust deed for Taiwan court" | `/legal-pathways:legal-translation` |
| "Ensure sales practices meet regulatory requirements" | `/cross-border-wealth:salecraft-compliance` |

## Self-Verification Protocol

Every skill follows a verification discipline:
1. Source every claim with provenance tags
2. Verify user-stated facts against available sources
3. Currency check via web search for time-sensitive positions
4. Cross-jurisdiction consistency for multi-jurisdiction structures
5. Substance reality check for every entity
6. Enforcement reality check — capture the gap between official policy and practice
7. Treaty shopping check (LOB/PPT) for every treaty benefit claimed

## Managed Agent Cookbooks

The `scripts/cookbooks/` directory contains headless agent configurations for automated workflows:

| Cookbook | Description |
|---|---|
| `regulatory-monitor/` | Daily regulatory change monitoring across target jurisdictions with subagents for scanning, treaty detection, and compliance alerting |

See `scripts/cookbooks/regulatory-monitor/agent.yaml` for the orchestration configuration.

## Contributing

Contributions welcome. Please open an issue before submitting a pull request for major changes.

### Setup

```bash
# Clone
git clone https://github.com/Zereo0317/legal-engineering-public.git
cd legal-engineering-public

# Install the Westlaw MCP server dependencies
cd westlaw-mcp && pip install -e . && cd ..

# Validate plugin structure
python3 scripts/validate.py
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WESTLAW_USERNAME` | No | Westlaw OnePass username |
| `WESTLAW_PASSWORD` | No | Westlaw OnePass password (sensitive) |
| `WESTLAW_BASE_URL` | No | Institution WAYFless or EZproxy URL |
| `WESTLAW_CLIENT_ID` | No | Westlaw Client ID |
| `INSTITUTION_SSO_DOMAIN` | No | Your institution's SSO domain (e.g. `idm.example.edu`) |
| `COURTLISTENER_API_KEY` | No | CourtListener API key (higher rate limits) |
| `CONGRESS_API_KEY` | No | Congress.gov API key |
| `SEC_EDGAR_EMAIL` | No | Email for SEC EDGAR User-Agent compliance |

Most tools work without any API keys using free public APIs (CourtListener, Federal Register, eCFR, EUR-Lex, Taiwan Judicial Yuan, OECD, SEC EDGAR, Singapore eLitigation).

## Disclaimer

This software is for educational and research purposes only. It does not provide legal advice. No attorney-client relationship is created by using this software. Always consult qualified legal professionals for legal matters.

## License

MIT License. See individual reference files for data provenance and attribution.
