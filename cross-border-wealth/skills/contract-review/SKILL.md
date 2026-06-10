---
name: contract-review
description: >
  This skill should be used when the user asks to review a contract, analyze an
  agreement, check contract terms, or generate a redline. Reviews contracts
  against market standards with dual severity scoring for legal risk and business
  friction. Covers NDAs, vendor agreements, SaaS MSAs, and engagement letters.
  Flags over-lawyering as a failure mode. Can produce redline DOCX output when
  python-docx is available.
argument-hint: '[NDA | vendor agreement | SaaS MSA | engagement letter | paste contract]'
tools:
  - westlaw_search_cases
  - westlaw_search_eu_law
  - web_search
categories:
  - contracts
  - review
  - commercial
version: 0.1.0
---

# /contract-review

Reviews contracts with a dual-axis assessment: legal risk AND business friction. Over-lawyering is treated as a failure mode. Supports tracked-changes-style redline output.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Identify contract type and context.** Determine:
   - Contract type: NDA, vendor agreement, SaaS MSA, engagement letter, other
   - Your client's position: buyer/seller, discloser/recipient, service provider/customer
   - Deal value and strategic importance (affects proportionality threshold)
   - Jurisdiction and governing law
   - Any specific concerns the user has flagged

3. **Clause-by-clause analysis.** For each material clause, assess on DUAL axes:

   ### Legal Risk (what could go wrong legally)
   - 🔴 **Critical** — Exposes client to existential/uncapped liability, regulatory breach, IP loss
   - 🟠 **High** — Material financial exposure, difficult to unwind, litigation risk
   - 🟡 **Medium** — Suboptimal but manageable; common in negotiated agreements
   - 🟢 **Low** — Minor concern; rarely litigated; standard market terms

   ### Business Friction (cost of pushing back)
   - ⛔ **Blocking** — Counterparty will walk; this is their non-negotiable
   - 🟠 **Significant** — Will require escalation; may delay deal 2+ weeks
   - 🟡 **Moderate** — Standard negotiation point; counterparty expects pushback
   - 🟢 **Minor** — Easy win; counterparty typically concedes without escalation

4. **Market standard comparison.** For each flagged clause:
   - What does the market standard look like for this deal type/size?
   - Is this clause within the range of reasonable? (even if not ideal)
   - Who has leverage in this negotiation?

5. **Proportionality filter.** Before flagging, ask:
   - Is the risk proportionate to the deal value?
   - Would a reasonable in-house counsel at a well-run company flag this?
   - Is pushing back worth the relationship cost and deal delay?
   - **If NO → do not flag.** Note it as "acceptable for deal size" and move on.

6. **Produce review output:**

   ### Executive Summary
   - Overall assessment: Ready to sign / Sign with minor changes / Needs negotiation / Do not sign
   - Top 3 issues requiring attention
   - Estimated negotiation effort

   ### Clause Review Table

   | # | Clause | Legal Risk | Business Friction | Action | Priority |
   |---|---|---|---|---|---|
   | 1 | Indemnification (§7.2) | 🔴 Critical | 🟡 Moderate | Redline: cap at 2x fees | 1 |
   | 2 | IP assignment (§4.1) | 🟠 High | 🟠 Significant | Negotiate: carve-out for pre-existing IP | 2 |
   | 3 | Auto-renewal (§9.3) | 🟡 Medium | 🟢 Minor | Redline: add 60-day notice | 3 |
   | 4 | Governing law (§12) | 🟢 Low | ⛔ Blocking | Accept: not worth the fight | — |

   ### Red Flags (🔴 must address before signing)
   ### Amber Flags (🟠 should address if possible)
   ### Green Flags (🟢 acceptable as-is)

7. **Anti-over-lawyering check.** Review your own output:
   - Are there more than 5 redline requests? If so, prioritize ruthlessly.
   - Is any flagged issue disproportionate to the deal value?
   - Would these comments make the client look unreasonable?
   - Consolidate and trim.

8. **Offer next steps:**
   > 1. **Redline DOCX** — I'll produce a Word document with tracked-changes formatting
   > 2. **Redline Markdown** — I'll produce a text-based diff of changes
   > 3. **Negotiation talking points** — key arguments for your top 3 asks
   > 4. **Alternative language** — I'll draft replacement clauses for flagged items
   > 5. **Comparison** — I'll compare this against [another contract / template]
   > 6. **Risk acceptance memo** — document why you're accepting specific risks

## Output Formats

This skill supports multiple output formats for redline documents:

### DOCX Redline (preferred)
Check availability: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/check_docx.sh`

Generate redline: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate_redline.py --original <original.txt> --revised <revised.txt> --output <redline.docx>`

Produces a Word document with:
- Red strikethrough for deleted text
- Blue underline for added text
- Professional formatting with headers and metadata

### Markdown Diff (fallback)
If python-docx is not available, the redline falls back to markdown diff format:
- `~~deleted text~~` for removals
- **`added text`** (bold) for additions
- Side-by-side comparison where possible
