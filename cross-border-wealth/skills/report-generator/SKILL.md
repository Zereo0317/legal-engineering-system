---
name: report-generator
description: >
  This skill should be used when the user asks to generate a report, render
  analysis as HTML, create a document from findings, or export results. Produces
  standalone HTML reports with interactive diagrams, jurisdiction matrices, risk
  heat maps, and compliance dashboards. Supports DOCX and PDF output when
  dependencies are available.
argument-hint: '[analysis to render | "from last analysis" | report type]'
tools:
  - web_search
categories:
  - output
  - reports
  - documents
version: 0.1.0
---

# /report-generator

Converts any analysis into a professional, interactive HTML report. Self-contained single-file output with no external dependencies. Supports multiple output formats with graceful degradation.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` for house style and output preferences.

2. **Get the analysis.** From $ARGUMENTS or the most recent analysis output in this conversation. If no analysis available, ask what to report on.

3. **Determine report type:**
   - **Structure Report** — entity diagram (SVG), flow analysis, dimension scores, optimization roadmap
   - **Jurisdiction Comparison** — sortable matrix, heat map, radar charts per jurisdiction
   - **Treaty Route Map** — flow diagram showing treaty paths, WHT at each leg, total cost
   - **Risk Dashboard** — heat map, risk-by-risk panels, mitigation tracker, timeline
   - **Compliance Dashboard** — regime checklist, gap flags, deadline calendar
   - **Research Memo** — formatted research with linked citations, authority table
   - **Case Atlas** — interactive case panels with filters, expandable sections
   - **Custom** — user specifies the format

4. **Check output capabilities.** Run `${CLAUDE_PLUGIN_ROOT}/scripts/check_dependencies.sh` to detect available output formats:
   - **HTML** (always available) — default output, uses bundled template
   - **DOCX** — available if python-docx is installed; run `${CLAUDE_PLUGIN_ROOT}/scripts/html_to_docx.py` to convert
   - **PDF** — available if wkhtmltopdf is installed; convert from HTML

5. **Build the HTML report.** Copy the template from `${CLAUDE_PLUGIN_ROOT}/assets/report-template.html` to the output location, then use Edit to inject content into the placeholder zones:
   - `<!-- AGENT: executive-summary -->` — executive summary section
   - `<!-- AGENT: structure-diagram -->` — SVG diagrams and structure visuals
   - `<!-- AGENT: jurisdiction-matrix -->` — sortable comparison tables
   - `<!-- AGENT: risk-heatmap -->` — risk visualization grid
   - `<!-- AGENT: recommendations -->` — action items and next steps

6. **Design principles:**
   - **Self-contained**: no CDN links, no external fonts, no API calls. Everything inline.
   - **Print-friendly**: CSS `@media print` rules for clean PDF export
   - **Accessible**: semantic HTML, ARIA labels, keyboard-navigable tables
   - **Responsive**: works on desktop, tablet, and mobile
   - **Dark/light mode**: respects `prefers-color-scheme`
   - **Culturally adapted**: language, date format, number format from practice profile

7. **Convert to additional formats** (if requested and available):
   - DOCX: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/html_to_docx.py <input.html> <output.docx>`
   - PDF: `wkhtmltopdf <input.html> <output.pdf>`
   - If a format is unavailable, inform the user with install instructions.

8. **Write the file.** Save to the matter workspace if active, otherwise to the current working directory. Filename: `[report-type]-[date].html`.

9. **Offer delivery options:**
   > **Report generated. Deliver it?**
   > 1. **Open in browser** — the file is at [path]
   > 2. **Email** — I'll send it via Gmail to [recipient]
   > 3. **Save to Drive** — I'll upload to [Google Drive folder]
   > 4. **Export as DOCX** — convert to Word format
   > 5. **Export as PDF** — convert to PDF
   > 6. **Just the file** — already saved at [path]

## Security

- HTML-escape all content from external sources (MCP results, uploaded documents, user inputs)
- Set cell text via `textContent`, never `innerHTML`
- Scheme-check URLs before emitting into `href`/`src` (allow `http:`, `https:`, `mailto:` only)
- No inline event handlers from dynamic content
- CSP meta tag: `default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'`
