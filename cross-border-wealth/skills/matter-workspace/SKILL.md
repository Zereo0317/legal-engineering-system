---
name: matter-workspace
description: >
  Manage per-client or per-matter workspaces. Isolates work product, verification
  logs, and compliance tracking per engagement. Essential for multi-client
  practices to prevent cross-contamination.
argument-hint: '[new <name> | list | switch <name> | close <name> | none]'
tools: []
categories:
  - workspace
version: 0.1.0
---

# /matter-workspace

Manages per-matter workspaces for multi-client practices.

## Instructions

1. **Read practice profile.** Load `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` → `## Matter Workspaces`.

2. **Handle the command:**
   - `new <name>` → create a new matter workspace at `~/.claude/plugins/config/legal-engineering/cross-border-wealth/matters/<slug>/`
   - `list` → show all workspaces with status
   - `switch <name>` → set the active matter
   - `close <name>` → archive a matter workspace
   - `none` → work at practice level (no matter isolation)

3. **New workspace contents:**
   - `matter.md` — matter-specific facts, parties, engagement scope, overrides
   - `verification-log.md` — per-matter verification log
   - `outputs/` — deliverables for this matter
   - `notes/` — working notes

4. **When a workspace is active**, all skills write outputs to the matter folder and read matter-specific context from `matter.md`. Cross-matter access is off by default.
