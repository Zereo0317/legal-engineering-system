# Westlaw MCP Server

Unified legal research MCP server combining 11 legal databases into 25 tools.

## Databases

| Source | Tools | Auth | Coverage |
|---|---|---|---|
| Westlaw Classic | `westlaw_classic_search`, `westlaw_classic_get_document` | Institutional subscription | US/UK/intl case law, statutes, regulations |
| CourtListener | `westlaw_search_cases`, `westlaw_get_case` | Free (optional API key) | US case law, 3,352 courts |
| Congress.gov | `westlaw_search_legislation` | Free API key | US legislation and bills |
| Federal Register | `westlaw_search_regulations` | None | US federal regulations, executive orders |
| eCFR | `westlaw_get_cfr_section` | None | Code of Federal Regulations full text |
| EUR-Lex | `westlaw_search_eu_law` | None | EU regulations, directives, decisions |
| Taiwan Judicial Yuan | 3 tools | None | Taiwan court judgments, statutes, interpretations |
| EU Compliance | 3 tools | None | GDPR, AI Act, DSA, DMA, NIS2, DORA |
| OECD Tax Treaties | 4 tools | None | Bilateral tax treaties, model convention, MLI status |
| SEC EDGAR | 3 tools | None | SEC filings, full-text search |
| Singapore eLitigation | 2 tools | None | Singapore court judgments |

Plus `westlaw_unified_search` (parallel multi-source) and `westlaw_health_check`.

## Installation

```bash
# Install dependencies
pip install -e .

# Run as MCP server (stdio)
python -m westlaw_mcp

# Or configure in .mcp.json (already set up in the plugins)
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `WESTLAW_USERNAME` | No | Westlaw OnePass username |
| `WESTLAW_PASSWORD` | No | Westlaw OnePass password |
| `WESTLAW_BASE_URL` | No | WAYFless or EZproxy URL for institutional access |
| `WESTLAW_CLIENT_ID` | No | Westlaw institutional client ID |
| `INSTITUTION_SSO_DOMAIN` | No | Your institution's SSO domain (e.g. `idm.example.edu`) |
| `COURTLISTENER_API_KEY` | No | CourtListener API key (free, for higher rate limits) |
| `CONGRESS_API_KEY` | No | Congress.gov API key (free at api.congress.gov) |
| `SEC_EDGAR_EMAIL` | No | Email for SEC EDGAR User-Agent compliance |

Without Westlaw Classic credentials, the server falls back to free sources for case law searches. Most tools (20 of 25) work without any credentials.

## Architecture

- **FastMCP** framework with Pydantic v2 input validation
- **Circuit breaker** pattern for resilient API calls (per-service state tracking)
- **Retry with exponential backoff** for transient failures
- **Playwright-based Westlaw scraper** with institutional SSO + CAPTCHA handling
- **Unified search** queries all sources in parallel and merges results

## License

MIT
