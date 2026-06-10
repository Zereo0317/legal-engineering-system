---
name: cold-start-interview
description: >
  Onboard a new user or practice. Interviews you about your practice type,
  jurisdiction footprint, structure inventory, risk posture, compliance
  obligations, cultural context, and output preferences. Writes the practice
  profile that every other skill reads. Takes 5-15 minutes depending on
  complexity. Run this first.
argument-hint: '[--redo | --quick | --check-integrations | --section <name>]'
tools:
  - westlaw_health_check
  - web_search
categories:
  - workspace
version: 0.1.0
---

# /cold-start-interview

Builds the practice profile at `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` by interviewing the user. Every other skill in this plugin reads this file before doing anything.

## Instructions

1. **Check for existing profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`. If it exists and is populated (no `[PLACEHOLDER]` in the first 5 sections), tell the user: "You already have a practice profile. Run `/cross-border-wealth:cold-start-interview --redo` to start over, or `/cross-border-wealth:customize` to edit specific sections."

   If `$ARGUMENTS` contains `--redo`, proceed from scratch. If `--quick`, do the abbreviated version (steps 2-4 only). If `--check-integrations`, jump to step 8. If `--section <name>`, jump to that section.

2. **Practice identity.** Ask conversationally — don't present a form:

   "Let's set up your practice profile. This takes 5-15 minutes and makes everything else in this plugin work better.

   First: what kind of practice are you? (Private wealth advisory, family office, tax litigation, Big Four, boutique international tax, in-house, academic, or something else?) And where are you based?"

   From the answer, fill: practice type, jurisdiction of establishment, primary clients.

3. **The pain.** "What's the thing that hurts most in your practice right now? The thing you wish you could fix?" Record verbatim.

4. **Who's using this.** "Are you a tax adviser or lawyer yourself, or are you a non-lawyer working with one? And what language(s) do you work in with your clients?"

   From the answer, fill: role, attorney contact, language preferences.

5. **Cultural context.** Based on the languages and client types mentioned, infer and confirm the cultural context. Don't ask "what's your cultural context?" — instead: "It sounds like you work primarily with [inferred context — e.g., Greater China family enterprises]. Is that right, or is there a better way to describe your client base?"

6. **Jurisdiction footprint.** "Now the important part: jurisdictions. Let's map where your clients live, operate, and hold structures.

   Start with the primary jurisdictions — where are your clients tax resident? Where do they have real operations?"

   Then: "And the structuring jurisdictions — where do they hold entities for structural reasons? (Common ones: BVI, Cayman, Singapore, Luxembourg, Ireland, Netherlands, Hong Kong, Delaware, UAE...)"

   Build the jurisdiction footprint table and treaty network table. For each treaty pair, ask: "Which treaty benefits are you relying on?"

7. **Structure inventory.** "Do you have any existing structures you'd like to map? I'll draw them as diagrams. You can describe them however you like — org chart, narrative, or just the entity names and their relationships."

   For each structure, build the ASCII diagram and fill: purpose, tax efficiency target, key risk.

8. **Risk posture.** "How aggressive are your clients' positions generally? I need to calibrate my analysis.

   On substance: do all your entities have real substance, or are some shell entities?
   On treaty shopping: do you use entities primarily for treaty access?
   On transfer pricing: full documentation, or informal?
   On disclosure: do you disclose everything, or do you take positions on what's reportable?"

   Fill the risk posture section. If any answer suggests aggressive or reportable positions, note it without judgment — the plugin calibrates to the practice, it doesn't moralize.

9. **Compliance obligations.** "Which reporting regimes apply to your structures?" Present the table and check each: CRS, FATCA, DAC6, BEPS CbCR, UBO registers, local TP documentation, estate/inheritance tax, trust registration.

10. **Integrations.** Test each available integration:
    - Westlaw Classic: attempt a test query
    - CourtListener: attempt a test query
    - Google Drive: check connection
    - Slack: check connection
    - Gmail: check connection
    Fill the integration status table.

11. **House style.** "Last section: how do you want your deliverables?

    What tone? (Direct and confident, cautious and hedged, academic, or something else?)
    What format? (HTML reports, PDF, Markdown, or all three?)
    Where should work product go? (Google Drive, Slack, email, or just inline?)"

12. **Write the profile.** Copy the template from `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`, replace all `[PLACEHOLDER]` values with the interview answers, and write to `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

    Also write `~/.claude/plugins/config/legal-engineering/company-profile.md` with the practice-level details that would be shared across plugins.

13. **Confirm.** Show the user a summary of what was captured and offer: "Want to adjust anything? You can always edit the profile later with `/cross-border-wealth:customize` or re-run this interview with `/cross-border-wealth:cold-start-interview --redo`."

## Interview Style

- Conversational, not form-filling. One topic at a time.
- Adapt language to the user's apparent level. A Big Four partner knows what PPT means; a founder's assistant may not.
- If the user gives short answers, that's fine — fill what you can, flag what's missing.
- If the user gives detailed answers, capture the detail — it's gold for calibrating the plugin.
- Never judge the risk posture. The plugin serves the practice as configured.
- For multilingual users, conduct the interview in their preferred language but write the profile in English (the skills read English). Note the language preferences so deliverables can be generated in the client's language.
