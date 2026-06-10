---
name: legal-dashboard
description: >
  This skill should be used when the user asks to create a legal dashboard,
  compliance overview, matter status board, or interactive jurisdiction
  comparison. Generates self-contained HTML dashboards with live filtering,
  sorting, and risk visualization.
argument-hint: '[dashboard type | "compliance" | "matter status" | "jurisdiction comparison"]'
tools:
  - web_search
categories:
  - output
  - dashboards
  - compliance
  - visualization
version: 0.1.0
---

# /legal-dashboard

Generates interactive, self-contained HTML dashboards for legal practice management. Single-file output with inlined CSS and JS — no external dependencies required.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` for house style and output preferences.

2. **Determine dashboard type.** From $ARGUMENTS or by asking the user. Supported presets:

   ### Cross-Border Structure Overview
   - Entity hierarchy with jurisdiction flags
   - Fund flow diagrams with treaty rates
   - Risk indicators per entity
   - Compliance status per jurisdiction

   ### Compliance Dashboard
   - Regime-by-regime compliance status grid
   - Filing deadline tracker with countdown
   - Gap analysis visualization
   - Risk heat map by jurisdiction and regime

   ### Matter Status Board
   - Active matters with status indicators
   - Deadline timeline
   - Team assignments
   - Priority sorting

   ### Custom Dashboard
   - User specifies data and layout requirements

3. **Build the dashboard.** Copy the template from `${CLAUDE_PLUGIN_ROOT}/assets/dashboard-template.html` to the output location, then use Edit to inject content into placeholder zones:
   - `<!-- AGENT: dashboard-title -->` — dashboard title and description
   - `<!-- AGENT: sidebar-nav -->` — navigation items for sidebar
   - `<!-- AGENT: matter-list -->` — matter cards or entity list
   - `<!-- AGENT: compliance-grid -->` — compliance status grid
   - `<!-- AGENT: deadline-tracker -->` — upcoming deadlines table
   - `<!-- AGENT: risk-heatmap -->` — risk visualization
   - `<!-- AGENT: summary-stats -->` — top-level KPI cards

4. **Design principles:**
   - **Self-contained**: no CDN links, no external fonts, no API calls
   - **Interactive**: filterable by jurisdiction, risk level, status; sortable tables
   - **Print-friendly**: CSS `@media print` for clean export
   - **Accessible**: ARIA labels, keyboard navigation, screen reader friendly
   - **Dark theme default**: professional legal styling, respects `prefers-color-scheme`
   - **Color-coded risk**: red (critical), amber/orange (high), yellow (medium), green (low)

5. **Write the file.** Save to the matter workspace if active, otherwise to the current working directory. Filename: `[dashboard-type]-dashboard-[date].html`.

6. **Offer next steps:**
   > 1. **Open in browser** — the file is at [path]
   > 2. **Add data** — I'll populate with specific matter/entity data
   > 3. **Customize** — adjust layout, add/remove sections
   > 4. **Export** — save as PDF via print dialog
   > 5. **Just the file** — already saved at [path]

## Security

- HTML-escape all injected content
- Set cell text via `textContent`, never `innerHTML`
- Scheme-check URLs (`http:`, `https:`, `mailto:` only)
- CSP meta tag: `default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'`
