---
name: action-executor
description: >
  Execute actions beyond analysis — send reports via Gmail, post to Slack, save
  to Google Drive, run web searches, fetch documents, create GitHub issues. The
  "do it" skill that turns analysis into action. Always confirms before executing.
argument-hint: '[action description | "send report to X" | "save to Drive" | "post to Slack"]'
tools:
  - westlaw_classic_search
  - web_search
  - web_fetch
categories:
  - workspace
version: 0.1.0
---

# /action-executor

Executes actions using connected MCP tools and integrations. Turns analysis into action — send, save, post, search, fetch.

## Instructions

1. **Load practice profile.** Read `~/.claude/plugins/config/legal-engineering/cross-border-wealth/CLAUDE.md` for integration status and preferences.

2. **Determine the action.** From $ARGUMENTS:

   | Action | Tool | Requirements |
   |---|---|---|
   | Send report via email | Gmail MCP | Recipient, subject, body, attachment |
   | Post update to Slack | Slack MCP | Channel, message |
   | Save to Google Drive | Google Drive MCP | Folder, filename, content |
   | Search for legal authority | Westlaw MCP / web search | Query |
   | Fetch a document | Web fetch | URL |
   | Create a research task | GitHub MCP | Repo, issue title, body |

3. **Confirm before executing.** Always show the user exactly what will happen:

   ```
   I'll [action description]:
   - To: [recipient/destination]
   - Content: [summary of what will be sent/saved/posted]
   - Attachments: [if any]

   Proceed? (yes / no / edit)
   ```

4. **Destination check.** Before sending any output:
   - Is this privileged content going to a non-privileged destination?
   - Is this client-specific content going to a channel visible to other clients?
   - Is this tax advice going to someone who isn't the client?
   Flag any destination concerns.

5. **Execute the action.** Use the appropriate MCP tool. Report the result.

6. **Log the action.** Record what was sent, where, when, and by whom in the matter workspace (if active).

## Safety

- **Never send without confirmation.** Every action is proposed, then confirmed, then executed.
- **Never send privileged content to non-privileged destinations** without explicit override.
- **Never send to external recipients** (opposing counsel, regulators, counterparties) without double confirmation.
- **Log everything.** Every action is recorded for audit trail.
