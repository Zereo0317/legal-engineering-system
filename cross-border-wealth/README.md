# Cross-Border Wealth & Tax

Claude Code plugin for cross-border wealth structuring, tax litigation research, and multi-jurisdiction entity architecture.

## Installation

```bash
claude plugin install cross-border-wealth --source ./cross-border-wealth
```

## First Run

```bash
/cross-border-wealth:cold-start-interview
```

This interviews you about your practice — jurisdiction footprint, structure inventory, risk posture, compliance obligations, cultural context, and output preferences. Takes 5-15 minutes. Every other skill reads the resulting practice profile.

## MCP Connections

The plugin connects to Westlaw Classic MCP for legal research. Set these at install time or in `.mcp.json`:

- `WESTLAW_CLIENT_ID` — institutional client ID
- `WESTLAW_USERNAME` / `WESTLAW_PASSWORD` — institutional credentials
- `WESTLAW_BASE_URL` — WAYFLESS URL for institutional access
- `COURTLISTENER_API_KEY` — CourtListener API key (free at courtlistener.com)
- `CONGRESS_API_KEY` — Congress.gov API key (free at api.congress.gov)

Without institutional Westlaw access, the plugin falls back to CourtListener (US case law), EUR-Lex (EU law), Federal Register, and eCFR — all free.

## Cultural Adaptation

The plugin adapts communication style and analysis framing to the client's cultural context:
- Greater China family enterprises (接班/succession, family harmony)
- Gulf wealth (Sharia compliance, family governance)
- European old wealth (privacy, generational preservation)
- Silicon Valley founders (speed, optionality, exit planning)
- Latin American industrial families (political risk, currency diversification)
- Southeast Asian tycoons (multi-jurisdiction operations, family conglomerates)

Set the cultural context during the cold-start interview or via `/cross-border-wealth:customize`.
