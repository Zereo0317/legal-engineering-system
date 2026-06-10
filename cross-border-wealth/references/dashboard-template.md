# Dashboard Template

Standard format for data-heavy outputs. Used by `/cross-border-wealth:report-generator`.

## Structure

1. **Summary stats line** — the most valuable part. A reader should know the shape of the data in 3 seconds.
   - Example: "12 jurisdictions scanned · 3 recommended · 2 flagged · avg effective rate 8.2%"
   - Example: "6 risks identified · 2 critical · 3 elevated · 1 low"

2. **One table** — sortable, filterable. Columns vary by report type.

3. **One or two charts max** — risk heat map, jurisdiction comparison radar, treaty route flow diagram. Keep it simple.

4. **Reviewer note** — carried over from the analysis.

## Security Rules

- All cell values from external sources (MCP results, user uploads, counterparty data) are HTML-escaped before rendering
- Cell text is set via `textContent`, never `innerHTML`
- URL scheme-check before `href`/`src`: allow `http:`, `https:`, `mailto:` only
- No formula injection (for Excel outputs): prefix cells starting with `=`, `+`, `-`, `@` with a single quote
- No inline event handlers from dynamic content

## When to Offer

Offer a dashboard when output has:
- More than ~10 rows of tabular data
- Any data with severity, status, or date columns
- Portfolio / register / tracker / checklist / findings list

Don't offer for: a 3-item issue list, a memo, a redline, a client letter.
