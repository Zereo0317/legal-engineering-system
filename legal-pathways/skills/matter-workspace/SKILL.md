---
name: matter-workspace
description: >
  Create and manage structured matter workspaces for legal projects. Tracks
  deadlines, parties, documents, and correspondence with cross-session memory.
  Enforces privacy boundaries between matters.
argument-hint: '["new" | matter-name | "list" | "archive"]'
tools: []
categories:
  - project-management
  - organization
  - workflow
version: 0.1.0
---

# /matter-workspace

Creates and manages structured workspaces for legal matters. Each matter gets its own directory with tracked deadlines, parties, documents, and correspondence. Cross-session memory via matter.md ensures continuity across conversations. Privacy boundaries prevent information leakage between matters.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/legal-pathways/CLAUDE.md`.

2. **Determine action:**
   - `new` — Create a new matter workspace
   - `[matter-name]` — Open existing matter, load context
   - `list` — Show all active matters with status
   - `archive` — Move matter to archived state

3. **Creating a new matter (`new`):**

   ### Interview for matter setup:
   - Matter name / short code (e.g., "CHEN-IMMIGRATION-2024")
   - Matter type: immigration, credential, corporate, litigation, advisory, other
   - Client name (or pseudonym for privacy)
   - Key parties involved
   - Primary objective
   - Key deadlines (filing dates, expiry dates, statute of limitations)
   - Budget (if applicable)
   - Conflict check: does this matter conflict with any existing matter?

   ### Create directory structure:
   ```
   ~/.claude/matters/[MATTER-CODE]/
   ├── matter.md              # Cross-session memory file
   ├── deadlines.md           # All deadlines with status
   ├── parties.md             # All parties and contacts
   ├── correspondence/        # Logs of key communications
   │   └── .gitkeep
   ├── documents/             # Document index and notes
   │   └── .gitkeep
   ├── research/              # Legal research notes
   │   └── .gitkeep
   ├── strategy/              # Strategy memos and decisions
   │   └── .gitkeep
   └── billing/               # Time and cost tracking
       └── .gitkeep
   ```

4. **matter.md format** (the cross-session memory file):

   ```markdown
   # [MATTER-CODE]: [Matter Name]

   ## Status: [Active | On Hold | Pending [Action] | Archived]

   ## Quick Context
   [2-3 sentence summary for fast context loading]

   ## Key Facts
   - Client: [name/pseudonym]
   - Objective: [what we're trying to achieve]
   - Jurisdiction(s): [relevant jurisdictions]
   - Opposing/counterparty: [if applicable]
   - Budget: [amount/status]

   ## Current Phase
   [What stage is this matter at?]

   ## Next Actions
   - [ ] [Action 1] — due [date]
   - [ ] [Action 2] — due [date]
   - [ ] [Action 3] — due [date]

   ## Decision Log
   | Date | Decision | Rationale | Decided By |
   |---|---|---|---|
   | [date] | [decision] | [why] | [who] |

   ## Session History
   | Date | Session | Key Outcomes |
   |---|---|---|
   | [date] | [summary of what was done] | [outcomes] |

   ## Risks & Concerns
   - [Risk 1]
   - [Risk 2]

   ## Related Matters
   - [MATTER-CODE-2] (relationship: [type])
   ```

5. **Opening an existing matter:**
   - Read `~/.claude/matters/[MATTER-CODE]/matter.md`
   - Display: status, current phase, next actions, upcoming deadlines
   - Check for overdue deadlines and flag them 🔴
   - Offer to continue where last session left off

6. **Deadline management:**

   ### deadlines.md format:
   ```markdown
   # Deadlines: [MATTER-CODE]

   ## Upcoming
   | Date | Deadline | Type | Status | Notes |
   |---|---|---|---|---|
   | 2024-06-15 | File I-140 petition | Filing | 🟡 Pending | Need employer support letter |
   | 2024-07-01 | Respond to RFE | Regulatory | 🔴 Urgent | 30-day window |

   ## Completed
   | Date | Deadline | Completed | Notes |
   |---|---|---|---|
   | 2024-03-01 | Submit credential evaluation | 2024-02-28 | WES evaluation received |
   ```

   - Deadlines within 7 days: 🔴 Urgent
   - Deadlines within 30 days: 🟡 Approaching
   - Deadlines >30 days: 🟢 On track

7. **Privacy boundaries:**
   - NEVER reference information from Matter A when working on Matter B
   - NEVER list matter names from other matters (even for the same user)
   - Each matter workspace is treated as informationally isolated
   - Conflict check at creation only — after that, strict separation
   - If user asks to compare matters, explicitly confirm they want cross-matter analysis

8. **Session continuity protocol:**
   - At START of every session touching a matter: read matter.md
   - At END of every session: update matter.md with:
     - Session date and summary
     - Decisions made
     - Next actions updated
     - Any new deadlines added
     - Risks identified

9. **Offer next steps:**
   > 1. **Update** — update matter status, add deadline, log decision
   > 2. **Research** — start legal research for this matter (saved to research/)
   > 3. **Draft** — draft a document for this matter (saved to documents/)
   > 4. **Strategy** — develop or refine matter strategy
   > 5. **Timeline** — visual timeline of all deadlines and milestones
   > 6. **Handoff memo** — produce a matter summary for another advisor
   > 7. **Something else**
