---
name: customize
description: >
  Edit the practice profile directly. Change jurisdiction footprint, risk posture,
  structure inventory, compliance obligations, house style, or any other section.
  Faster than re-running the full cold-start interview.
argument-hint: '[section name | "add jurisdiction X" | "update risk posture" | "show profile"]'
tools: []
categories:
  - workspace
version: 0.1.0
---

# /customize

Edit the practice profile at `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

## Instructions

1. **Read the current profile.** Load `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md`.

2. **Determine the edit.** From $ARGUMENTS:
   - `show profile` → display the current profile
   - A section name → show and edit that section
   - A specific change → apply it directly (e.g., "add Singapore to jurisdiction footprint")
   - No argument → ask what to change

3. **Apply the edit.** Update the profile file. Show the user the before/after for the changed section.

4. **Confirm.** "Updated. This change applies to all skills immediately."
