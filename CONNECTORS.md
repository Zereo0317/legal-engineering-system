# Adding MCP Connectors

Guide for adding new MCP server connectors to the Legal Engineering plugin.

## Architecture

The plugin connects to legal data sources through MCP (Model Context Protocol) servers. Each connector is a standalone MCP server that exposes tools for searching and retrieving data from a specific source.

```
Plugin (skills, agents)
  ↓ calls tools via MCP protocol
MCP Server (e.g., westlaw_mcp)
  ↓ HTTP/scraping/API calls
Data Source (e.g., Westlaw Classic, CourtListener)
```

## Existing Connectors

| Connector | Client Module | Source | Auth | Transport |
|---|---|---|---|---|
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/westlaw_classic.py` | Westlaw Classic (institutional) | SAML SSO + Client ID | Playwright scraper |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/courtlistener.py` | CourtListener | API key (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/congress.py` | Congress.gov | API key (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/federal_register.py` | Federal Register | None (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/ecfr.py` | eCFR | None (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/eurlex.py` | EUR-Lex | None (free) | Web scraping + SPARQL |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/taiwan_judicial.py` | Taiwan Judicial Yuan | None (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/eu_compliance.py` | EU Compliance (GDPR/AI Act/DSA) | None (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/oecd_treaties.py` | OECD Tax Treaties | Optional API key | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/sec_edgar.py` | SEC EDGAR | None (free) | REST API (httpx) |
| `westlaw_mcp` | `westlaw-mcp/westlaw_mcp/clients/singapore_elit.py` | Singapore eLitigation | Optional API key | REST API (httpx) |
| Slack MCP | — | Slack | OAuth | HTTP/SSE |
| Google Drive MCP | — | Google Drive | OAuth | HTTP/SSE |

## Adding a New Connector

### Step 1: Choose the Pattern

**API-based connector** (recommended): Use when the source has a REST/GraphQL API.
- See `westlaw-mcp/westlaw_mcp/clients/courtlistener.py` or `westlaw-mcp/westlaw_mcp/clients/congress.py` as templates
- Uses `httpx` for HTTP requests with retry logic from `westlaw-mcp/westlaw_mcp/clients/base.py`

**Scraping-based connector**: Use when the source has no API.
- See `westlaw-mcp/westlaw_mcp/clients/westlaw_classic.py` as a template
- Uses `playwright` for browser automation
- Last resort — APIs are more reliable and maintainable

**SPARQL connector**: Use when the source exposes RDF/linked data.
- See `westlaw-mcp/westlaw_mcp/clients/eurlex.py` as a template

### Step 2: Create the Client

Create `westlaw-mcp/westlaw_mcp/clients/<source_name>.py`:

```python
"""<Source Name> API client."""
from __future__ import annotations

import os
from .base import api_request

BASE_URL = "https://api.example.com/v1"

async def search(query: str, limit: int = 20) -> dict:
    """Search for documents matching the query."""
    api_key = os.getenv("<SOURCE>_API_KEY", "")
    if not api_key:
        from ..errors import make_error
        return make_error("auth_missing", "<SOURCE>_API_KEY env var not set")

    params = {"q": query, "per_page": min(limit, 100)}
    headers = {"Authorization": f"Token {api_key}"}

    data = await api_request(
        "GET", f"{BASE_URL}/search",
        service_name="<source_name>",
        params=params, headers=headers,
    )
    if isinstance(data, dict) and data.get("error"):
        return data

    results = []
    for item in data.get("results", [])[:limit]:
        results.append({
            "title": item.get("title", ""),
            "citation": item.get("citation", ""),
            "date": item.get("date", ""),
            "url": item.get("url", ""),
            "snippet": item.get("snippet", ""),
        })

    return {
        "query": query,
        "count": len(results),
        "results": results,
        "source": "<Source Name>",
    }
```

### Step 3: Register the Circuit Breaker

In `westlaw-mcp/westlaw_mcp/clients/base.py`, add a circuit breaker entry:

```python
"<source_name>": {"failure_threshold": 5, "recovery_timeout": 30},
```

### Step 4: Add the Tool to server.py

In `westlaw-mcp/westlaw_mcp/server.py`, add a new tool function:

```python
@mcp.tool()
async def westlaw_search_<source>(
    query: str,
    limit: int = 20,
    response_format: str = "markdown",
) -> str:
    """Search <Source Name> for [description].

    Args:
        query: Search query
        limit: Maximum results (default 20)
        response_format: "markdown" or "json"
    """
    from .clients.<source_name> import search
    result = await search(query, limit=limit)
    if response_format == "json":
        return json.dumps(result, indent=2)
    return _format_results(result)
```

### Step 5: Add the Input Model

In `westlaw-mcp/westlaw_mcp/models.py`, add a Pydantic model:

```python
class SourceSearchInput(PaginationMixin):
    query: str = Field(..., min_length=1, description="Search query")
```

### Step 6: Register in .mcp.json

Add the required env var to `cross-border-wealth/.mcp.json`:

```json
"env": {
  ...,
  "<SOURCE>_API_KEY": "${user_config.<SOURCE>_API_KEY}"
}
```

And add the userConfig entry in `cross-border-wealth/.claude-plugin/plugin.json`:

```json
"userConfig": {
  ...,
  "<SOURCE>_API_KEY": {
    "type": "string",
    "description": "<Source Name> API key",
    "required": false
  }
}
```

### Step 7: Update the Unified Search

In `westlaw-mcp/westlaw_mcp/server.py`, add the new source to `westlaw_unified_search`:

```python
tasks.append(asyncio.create_task(
    clients.<source_name>.search(query, limit=limit)
))
```

### Step 8: Update Skill Routing

In `cross-border-wealth/skills/case-research/SKILL.md`, add a routing entry:

```markdown
| [Query Type] | `westlaw_search_<source>` | web search |
```

## Recommended Connectors to Add

| Priority | Source | Coverage | API | Cost |
|---|---|---|---|---|
| High | HKII (HK Inland Revenue) | Hong Kong tax rulings | Web scraping | Free |
| High | AustLII | Australian law | REST API | Free |
| Medium | OECD Tax Treaty Database | Treaty texts | Web/API | Free |
| Medium | IBFD (International Bureau of Fiscal Documentation) | Comparative tax | Institutional | Paid |
| Medium | Global Legal Monitor (LOC) | Worldwide legal developments | RSS/API | Free |
| Low | HKEX | HK company filings | REST API | Free |
| Low | ACRA (SG) | Singapore company registry | REST API | Paid |

## Testing

Test any new connector with:

```bash
# Run the health check
python -m westlaw_mcp
# Then call: westlaw_health_check

# Test the specific tool
# Call: westlaw_search_<source> with a known query
```

Verify that:
1. Circuit breaker trips correctly after repeated failures
2. Rate limiting is handled gracefully
3. Empty results return structured empty responses (not errors)
4. The tool works in both `markdown` and `json` response formats
