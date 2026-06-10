# Legal Engineering Platform — Commercial System Design

*Architecture for a production SaaS platform that monetizes the Legal Engineering
plugin while protecting IP, managing authentication, and providing persistent
user state. Deployed on GCP.*

*This document is the handoff spec for building the commercial product.
Separate repo: `legal-engineering-platform`.*

---

## 1. Design Principles

1. **Skills execute remotely, not on the client.** The proprietary SKILL.md logic
   never leaves our servers. Users interact through a thin plugin stub that calls
   our remote MCP server.
2. **Bring your own Westlaw.** Users authenticate with their own institutional or
   personal Westlaw credentials. We never purchase Westlaw access for them.
3. **Memory is cloud-native.** User profiles, progress, and session history persist
   in Firestore, accessible from any device.
4. **GCP-native.** Everything runs on Google Cloud Platform.
5. **MCP-first.** The remote server implements the MCP specification (2025-11-25)
   with OAuth 2.1 + PKCE authentication and Streamable HTTP transport.

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       User's Machine                         │
│                                                              │
│  Claude Code CLI / Desktop / Web                             │
│    └── legal-engineering-stub plugin (thin client)           │
│          ├── marketplace.json (public, no IP)                │
│          ├── stub SKILL.md files (invoke only, no logic)     │
│          └── .mcp.json → points to remote MCP server         │
│                  │                                           │
└──────────────────┼───────────────────────────────────────────┘
                   │ HTTPS (Streamable HTTP + OAuth 2.1)
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                    GCP Infrastructure                        │
│                                                              │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │ Cloud Run    │    │ Cloud Run    │    │ Firebase       │  │
│  │ (MCP Server) │◄──│ (API Gateway)│◄──│ Hosting        │  │
│  │              │    │              │    │ (Landing Page) │  │
│  │ - Skills     │    │ - Auth check │    │ - Sign up      │  │
│  │ - Agents     │    │ - Rate limit │    │ - Login        │  │
│  │ - References │    │ - Metering   │    │ - Dashboard    │  │
│  └──────┬───────┘    └──────────────┘    │ - Billing      │  │
│         │                                └────────────────┘  │
│  ┌──────┴───────┐    ┌──────────────┐    ┌────────────────┐  │
│  │ Westlaw MCP  │    │ Firestore    │    │ Secret Manager │  │
│  │ (legal       │    │              │    │                │  │
│  │  research)   │    │ - User state │    │ - Westlaw creds│  │
│  │              │    │ - Profiles   │    │ - API keys     │  │
│  │ Uses USER's  │    │ - Progress   │    │ - OAuth tokens │  │
│  │ credentials  │    │ - Sessions   │    │                │  │
│  └──────────────┘    └──────────────┘    └────────────────┘  │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │ Firebase Auth│    │ Cloud Logging│    │ Stripe         │  │
│  │              │    │ + BigQuery   │    │ (Billing)      │  │
│  │ - Email/pwd  │    │              │    │                │  │
│  │ - Google SSO │    │ - Usage logs │    │ - Subscriptions│  │
│  │ - GitHub SSO │    │ - Analytics  │    │ - Pay-per-use  │  │
│  └──────────────┘    └──────────────┘    └────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. IP Protection Architecture

### 3.1 The Two-Layer Plugin Pattern

**Public layer (distributed to users):**
```
legal-engineering-stub/           ← public repo, MIT license
  .claude-plugin/marketplace.json
  cross-border-wealth/
    .claude-plugin/plugin.json
    .mcp.json                     ← points to remote MCP server
    skills/
      structure-analysis/
        SKILL.md                  ← STUB: "invoke /structure-analysis"
      ...
  legal-pathways/
    skills/
      sovereign-architect/
        SKILL.md                  ← STUB: same pattern
      ...
```

Each stub SKILL.md contains ONLY:
```yaml
---
name: sovereign-architect
description: Design sovereign individual architecture (requires subscription)
argument-hint: '[goal]'
tools:
  - le_sovereign_architect      # remote MCP tool
---

# /sovereign-architect

This skill runs on the Legal Engineering cloud platform.

## Instructions

1. Call the `le_sovereign_architect` MCP tool with $ARGUMENTS
2. The tool handles all analysis, reference data lookup, and verification
3. Display the result to the user
```

**Private layer (runs on our servers):**
```
legal-engineering-server/         ← private repo, never distributed
  skills/                         ← full SKILL.md files with all logic
  references/                     ← all reference data
  agents/                         ← all agent definitions
  server.py                       ← MCP server that executes skills
  westlaw_mcp/                    ← Westlaw integration
```

### 3.2 How It Works

1. User installs the **stub plugin** (public, no IP)
2. Stub plugin connects to our **remote MCP server** via HTTPS
3. User authenticates via **OAuth 2.1 + PKCE** (Firebase Auth)
4. When user invokes a skill, the stub calls a remote MCP tool
5. The **server executes the full skill logic** server-side
6. Server reads reference data, runs Westlaw queries (using user's creds), applies verification protocol
7. Server returns the result to the user's Claude Code session
8. **The SKILL.md logic never leaves our servers**

### 3.3 What's Protected vs Exposed

| Component | Location | Accessible to user? |
|---|---|---|
| Stub SKILL.md (no logic) | User's machine | Yes — but contains no IP |
| Full SKILL.md (all logic) | Cloud Run server | No — never distributed |
| Reference data | Cloud Run server | No — served as tool output |
| MCP tool responses | User's machine | Yes — but this is the output, not the method |
| User's profile/state | Firestore | Yes — via API, it's their data |
| Westlaw credentials | GCP Secret Manager | No — encrypted at rest |

### 3.4 Prompt Injection Defense (Production)

**Layer 1: MCP Tool Input Validation**
- All MCP tool inputs validated by Pydantic v2 models
- Maximum input length enforced
- Known injection patterns filtered

**Layer 2: Skill Execution Isolation**
- Each skill execution runs in an isolated context
- Retrieved content (Westlaw results, web search) marked as DATA
- System prompt includes anti-injection directives

**Layer 3: Output Sanitization**
- Tool outputs stripped of any embedded instructions
- Source attribution added to all content
- User-facing output clearly delineated from system content

**Layer 4: Monitoring**
- All tool calls logged to Cloud Logging
- Anomaly detection on input patterns
- Rate limiting per user/per tool

**Reference**: [Prompt Obfuscation for LLMs (arXiv 2409.11026)](https://arxiv.org/abs/2409.11026)
— proposes embedding-space obfuscation. For our use case, the remote execution
model is more effective: the prompt never reaches the client at all.

---

## 4. Authentication System

### 4.1 User Authentication (Firebase Auth)

**Sign-up / Login Methods:**
- Email + password
- Google SSO
- GitHub SSO (developers, researchers)
- Apple SSO (future)

**User Types:**

| Type | Auth Flow | Capabilities |
|---|---|---|
| **Free** | Email signup | 5 skill invocations/day; free MCP tools only |
| **Student** | Email + .edu verification | 20 invocations/day; bring-your-own Westlaw |
| **Professional** | Email + payment | Unlimited; full features; priority |
| **Enterprise** | SSO + contract | Custom; team management; audit logs |

### 4.2 MCP Server Authentication (OAuth 2.1)

Following the MCP Authorization Specification (2025-11-25):

```
User's Claude Code
       │
       │  1. Discover OAuth metadata
       │     GET /.well-known/oauth-authorization-server
       │
       │  2. Authorization request (PKCE)
       │     GET /authorize?response_type=code
       │       &client_id={CIMD}&code_challenge={S256}
       │       &scope=skills:read+westlaw:use
       │       &resource=https://mcp.legal-engineering.com
       │
       │  3. User authenticates in browser (Firebase Auth)
       │     → Redirects back with authorization code
       │
       │  4. Token exchange
       │     POST /token (code + code_verifier)
       │     → Returns: access_token (15min) + refresh_token (90 days)
       │
       │  5. MCP tool calls with Bearer token
       │     POST /mcp (Authorization: Bearer {access_token})
       │
       │  6. Token refresh (automatic)
       │     POST /token (grant_type=refresh_token)
       ▼
Remote MCP Server (Cloud Run)
```

**Token Management:**
- Access tokens: 15 minutes, JWT, signed with RS256
- Refresh tokens: 90 days, rotated on each use, stored hashed (SHA-256) in Firestore
- Resource indicators (RFC 8707): tokens scoped to `https://mcp.legal-engineering.com`
- PKCE: Required for all clients (S256 only)

### 4.3 Westlaw Credential Management

**The user's Westlaw credentials are stored encrypted in GCP Secret Manager,
NOT in our database. We never see the plaintext password.**

```
User provides Westlaw credentials
       │
       │  1. Credentials encrypted client-side (optional)
       │     or transmitted over HTTPS to our API
       │
       │  2. API stores in GCP Secret Manager
       │     Secret name: users/{uid}/westlaw
       │     Encrypted at rest with Google-managed keys
       │     Access: only the Cloud Run service account
       │
       │  3. When a skill needs Westlaw:
       │     Cloud Run reads secret → passes to westlaw_mcp
       │     → westlaw_mcp authenticates to Westlaw
       │     → results returned to skill execution
       │     → credentials never logged or cached
       │
       │  4. User can revoke at any time
       │     DELETE /api/credentials/westlaw
       │     → Secret deleted from Secret Manager
       ▼
```

### 4.4 Institutional Westlaw Discovery

**API endpoint:** `GET /api/institutions/search?q={query}`

Database of known institutional Westlaw access points:

```json
{
  "institution": "Example University",
  "aliases": ["Example U", "EU"],
  "country": "US",
  "westlaw_access": {
    "available": true,
    "type": "EZproxy",
    "url_pattern": "https://ezproxy.lib.example.edu/login?url=https://1.next.westlaw.com",
    "auth_method": "institutional_sso",
    "instructions_en": "Library portal → Electronic Resources → Westlaw",
    "last_verified": "2026-05-23",
    "notes": "May require VPN if off-campus"
  }
}
```

**Discovery flow:**
1. User says "I'm at Example University"
2. System searches institution database
3. Returns access URL, instructions in user's language
4. Guides user through authentication
5. Tests connectivity and stores working credentials

**Data sources for building the institution database:**
- OCLC EZproxy stanza library
- OpenURL resolver databases
- Crowdsourced from users (with verification)

---

## 5. Memory & State System

### 5.1 Data Model (Firestore)

```
users/
  {uid}/
    profile/
      identity          # name, nationality, languages
      education          # degrees, institutions, evaluations
      experience         # professional background
      risk_posture       # conservative/moderate/aggressive
      cultural_context   # Greater China / Gulf / European / etc.

    cross_border_wealth/
      practice_profile   # full CLAUDE.md content (structured)
      structures[]       # structure inventory
      compliance         # compliance obligations
      integrations       # connected services

    legal_pathways/
      pathway_profile    # full CLAUDE.md content (structured)
      targets[]          # target credentials/statuses
      gaps[]             # identified gaps
      current_strategy   # chosen pathway approach

    projects/
      {project_id}/
        name
        type             # credential | immigration | aviation | wealth
        status           # active | paused | completed
        started_at
        target_date
        current_phase
        next_actions[]
        budget            # allocated / spent
        timeline_events[]
        notes[]

    sessions/
      {session_id}/
        started_at
        ended_at
        skills_used[]
        key_decisions[]
        research_findings[]
        progress_updates[]

    credentials/
      westlaw/           # reference to Secret Manager
        type             # onepass | institutional
        institution      # if institutional
        last_verified
        status           # active | expired | revoked

    preferences/
      language
      report_format
      tone
      timezone
```

### 5.2 Session Lifecycle

```
Session Start
  │
  ├── MCP server receives first tool call
  ├── Validate OAuth token → get user ID
  ├── Load user profile from Firestore
  ├── Load active projects
  ├── Check Westlaw credential status
  ├── Check for regulatory updates since last session
  │
  ├── Return context to Claude Code:
  │   "User: [name]. Active projects: [list].
  │    Last session: [date], worked on [summary].
  │    Westlaw: [connected/disconnected].
  │    Next actions: [list]."
  │
  └── Each subsequent tool call:
      ├── Execute skill logic server-side
      ├── Log to session history
      ├── Update project progress if applicable
      └── Return result

Session End (inferred from inactivity or explicit)
  │
  ├── Save session summary to Firestore
  ├── Update project progress
  └── Queue any follow-up tasks (treaty watch, regulatory alerts)
```

### 5.3 Cross-Device Sync

Because state lives in Firestore:
- User starts on laptop with Claude Code CLI → picks up on desktop app
- User starts on web (claude.ai/code) → continues on mobile
- Profile, projects, and progress are always current

---

## 6. Frontend (Separate Repo)

### 6.1 Repository: `legal-engineering-platform`

```
legal-engineering-platform/
  ├── frontend/                    # React + Vite + Tailwind
  │     ├── src/
  │     │     ├── pages/
  │     │     │     ├── Landing.tsx
  │     │     │     ├── Login.tsx
  │     │     │     ├── Signup.tsx
  │     │     │     ├── Dashboard.tsx
  │     │     │     ├── Settings.tsx
  │     │     │     ├── Projects.tsx
  │     │     │     └── Billing.tsx
  │     │     ├── components/
  │     │     ├── hooks/
  │     │     └── lib/
  │     │           ├── firebase.ts
  │     │           └── api.ts
  │     └── public/
  │
  ├── server/                      # Remote MCP server (Python)
  │     ├── mcp_server.py          # FastMCP with Streamable HTTP
  │     ├── auth.py                # OAuth 2.1 + Firebase token validation
  │     ├── skills/                # Full SKILL.md files (PRIVATE)
  │     ├── references/            # All reference data (PRIVATE)
  │     ├── agents/                # Agent definitions (PRIVATE)
  │     ├── westlaw_mcp/           # Westlaw integration
  │     ├── state.py               # Firestore state management
  │     ├── metering.py            # Usage tracking
  │     └── Dockerfile
  │
  ├── infra/                       # Terraform / GCP config
  │     ├── main.tf
  │     ├── cloud_run.tf
  │     ├── firestore.tf
  │     ├── secret_manager.tf
  │     └── firebase.tf
  │
  └── stub/                        # Public stub plugin (distributed)
        ├── .claude-plugin/
        ├── cross-border-wealth/
        │     └── skills/*/SKILL.md  # stubs only
        └── legal-pathways/
              └── skills/*/SKILL.md  # stubs only
```

### 6.2 Landing Page

**URL:** `https://legal-engineering.com` (or `.dev` / `.ai`)

**Sections:**
1. Hero: "Legal Engineering for Sovereign Individuals"
2. What it does: 3 use-case cards (wealth structuring, immigration, aviation)
3. How it works: Install → Connect → Use (3 steps)
4. Pricing: Free / Student / Professional / Enterprise
5. Sign Up: Firebase Auth (email/Google/GitHub)

**Tech stack:**
- React + Vite + Tailwind CSS
- Firebase Hosting (CDN, SSL, custom domain)
- Firebase Auth (client SDK)

### 6.3 Dashboard

After login, users see:
- Active projects with progress bars
- Quick-start buttons for common skills
- Westlaw connection status
- Usage meter (invocations used / remaining)
- Recent session history

---

## 7. Pricing Model

| Tier | Price | Invocations | Westlaw | Features |
|---|---|---|---|---|
| **Free** | $0 | 5/day | BYO only | Free sources, basic skills |
| **Student** | $9/mo | 50/day | BYO only | All skills, progress tracking |
| **Professional** | $49/mo | Unlimited | BYO only | All skills, priority, API access |
| **Enterprise** | Custom | Unlimited | BYO or managed | Team mgmt, SSO, audit, SLA |

**Billing**: Stripe Billing with Firebase Auth integration.
Usage metering via Cloud Logging → BigQuery → Stripe usage records.

---

## 8. GCP Services and Cost Estimate

### Services Used

| Service | Purpose | Estimated Monthly Cost |
|---|---|---|
| **Cloud Run** | MCP server + API | $50–$200 (per-request billing) |
| **Firestore** | User state, profiles, sessions | $10–$50 |
| **Secret Manager** | Westlaw credentials, API keys | $1–$5 |
| **Firebase Auth** | User authentication | Free (up to 50K MAU) |
| **Firebase Hosting** | Landing page, dashboard | Free–$25 |
| **Cloud Logging** | Audit, analytics, metering | $10–$50 |
| **BigQuery** | Usage analytics, billing data | $5–$20 |
| **Cloud Armor** | DDoS protection, WAF | $0–$50 |
| **Artifact Registry** | Docker images for Cloud Run | $1–$5 |
| **Total (early stage)** | | **$80–$400/month** |

### Scaling Considerations

- Cloud Run auto-scales to zero: no cost when not in use
- Firestore scales automatically with usage
- The main cost driver is Cloud Run CPU time during skill execution
- Westlaw API calls use the user's own credentials (no cost to us)

---

## 9. Security Checklist

### Data Protection
- [ ] All data encrypted at rest (GCP default)
- [ ] All data encrypted in transit (HTTPS everywhere)
- [ ] Westlaw credentials in Secret Manager (not Firestore)
- [ ] PII minimization: only collect what's needed
- [ ] Data deletion API: users can delete their account and all data
- [ ] GDPR compliance: data export, right to erasure

### Authentication
- [ ] OAuth 2.1 with PKCE (S256) for MCP server
- [ ] Firebase Auth for web UI
- [ ] Short-lived access tokens (15 min)
- [ ] Refresh token rotation
- [ ] Resource indicators (RFC 8707) to prevent token mis-redemption

### Infrastructure
- [ ] Cloud Run: no SSH, no persistent storage, auto-scales
- [ ] VPC: private networking between Cloud Run and Firestore
- [ ] IAM: principle of least privilege
- [ ] Cloud Armor: rate limiting, DDoS protection
- [ ] Dependency scanning: Snyk or Dependabot

### Application
- [ ] Input validation on all MCP tool inputs (Pydantic v2)
- [ ] Output sanitization on all tool responses
- [ ] Prompt injection detection (heuristic + LLM-based)
- [ ] Rate limiting per user per tool
- [ ] Audit logging for all state changes

---

## 10. Development Phases

### Phase 1: Stub Plugin + Remote MCP Server (4–6 weeks)

**Goal:** Skills execute remotely. IP is protected. Free tier works.

- [ ] Create `legal-engineering-platform` repo
- [ ] Build remote MCP server (FastMCP + Streamable HTTP on Cloud Run)
- [ ] Implement OAuth 2.1 + PKCE with Firebase Auth
- [ ] Port all 25 skills to remote execution
- [ ] Build stub plugin for distribution
- [ ] Deploy to Cloud Run
- [ ] Test end-to-end: install stub → authenticate → use skill

### Phase 2: State Management + Memory (2–3 weeks)

**Goal:** User state persists across sessions and devices.

- [ ] Implement Firestore data model
- [ ] Build profile sync (CLAUDE.md ↔ Firestore)
- [ ] Build progress tracker
- [ ] Implement session lifecycle hooks
- [ ] Test cross-device state sync

### Phase 3: Frontend + Billing (3–4 weeks)

**Goal:** Users can sign up, pay, and manage their account.

- [ ] Build landing page (React + Firebase Hosting)
- [ ] Implement login/signup (Firebase Auth)
- [ ] Build dashboard (projects, usage, settings)
- [ ] Integrate Stripe Billing
- [ ] Implement usage metering

### Phase 4: Westlaw Integration + Institution Discovery (2–3 weeks)

**Goal:** Seamless Westlaw credential management.

- [ ] Build credential storage in Secret Manager
- [ ] Build institutional discovery API + database
- [ ] Implement guided credential onboarding flow
- [ ] Test with multiple institution types
- [ ] Build credential health monitoring

### Phase 5: Polish + Launch (2–3 weeks)

**Goal:** Production-ready.

- [ ] Security audit
- [ ] Load testing
- [ ] Documentation
- [ ] Beta testing with 10–20 users
- [ ] Domain registration and DNS setup
- [ ] Launch

**Total: 13–19 weeks (3–5 months)**

---

## 11. Key Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| **MCP transport** | Streamable HTTP | Works behind load balancers; stateless; production-ready |
| **Auth** | OAuth 2.1 + PKCE via Firebase | MCP spec compliant; Firebase handles user management |
| **Credential storage** | GCP Secret Manager | Encrypted at rest; audited access; auto-rotation support |
| **State store** | Firestore | Serverless; real-time sync; scales automatically |
| **Compute** | Cloud Run | Scales to zero; per-request billing; Docker-based |
| **Frontend** | React + Vite | Fast; modern; good Firebase SDK support |
| **Hosting** | Firebase Hosting | CDN; SSL; custom domain; free tier |
| **Billing** | Stripe | Industry standard; good Firebase integration |
| **IP protection** | Remote execution | SKILL.md never leaves server; stub plugin has no logic |
| **Monitoring** | Cloud Logging + BigQuery | Native GCP; SQL analytics; alerting |

---

## 12. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Westlaw blocks our automation | Medium | High | Playwright anti-detection; rotate user agents; respect rate limits |
| User credential breach | Low | Critical | Secret Manager + encryption; minimal access; audit logs |
| Prompt injection extracts logic | Low | Medium | Remote execution means logic isn't on client; server-side guards |
| Claude Code changes plugin API | Medium | Medium | Version pinning; monitor Anthropic announcements |
| MCP spec changes break auth | Low | Medium | Follow spec closely; test with each Claude Code update |
| Low adoption | Medium | Medium | Free tier; strong reference data; target niche (legal engineering) |
| Thomson Reuters legal action | Low | High | We provide tools, not legal advice; user's own credentials; CFAA safe harbor |

---

## 13. Open Questions

1. **Domain name**: `legal-engineering.com` / `.dev` / `.ai`?
2. **Team**: Who builds the frontend? Who handles DevOps?
3. **Legal**: Terms of service, privacy policy, liability disclaimers
4. **Westlaw TOS**: Does automated access via user's credentials violate Westlaw TOS?
   Need legal review. The Playwright scraper pattern is common but not explicitly authorized.
5. **Data residency**: Where should Firestore data live? Choose region closest to
   primary user base, or multi-region for global coverage.
6. **Mobile**: Is a mobile app needed? Or is claude.ai/code sufficient?

---

## References

### Architecture
- [Host MCP servers on Cloud Run](https://docs.google.com/run/docs/host-mcp-servers) — Google Cloud
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — MCP Protocol
- [MCP OAuth 2.1 Implementation Guide](https://mcpplaygroundonline.com/blog/mcp-server-oauth-authentication-guide) — MCP Playground

### Security
- [Claude Code Security](https://code.claude.com/docs/en/security) — Anthropic
- [MCP Server Security Best Practices](https://www.digitalapplied.com/blog/mcp-server-security-best-practices-2026-engineering-guide) — Digital Applied
- [Prompt Obfuscation for LLMs](https://arxiv.org/abs/2409.11026) — Pape et al., USENIX Security 2025
- [MCP Credential Security Best Practices](https://www.doppler.com/blog/mcp-server-credential-security-best-practices) — Doppler

### Memory & State
- [Claude Code Memory](https://code.claude.com/docs/en/memory) — Anthropic
- [Claude Memory Bank](https://nsclass.github.io/2026/03/15/claude-memory-bank) — Community
- [Persistent Memory for Claude Code Agents](https://dev.to/whoffagents/how-to-build-persistent-memory-into-claude-code-agents-cross-session-identity-that-actually-works-41h4) — DEV

### Monetization
- [How to Monetize Claude Code Skills](https://www.agent37.com/blog/monetize-claude-code-skills) — Agent37
- [Private Plugin Marketplaces](https://gist.github.com/gwpl/103c997128c6b6a6102e2a4a6cf8d283) — Community
- [Claude Plugins Official](https://claude.com/plugins) — Anthropic

### Westlaw
- [Westlaw EZproxy Configuration](https://help.oclc.org/Library_Management/EZproxy/EZproxy_database_stanzas/Database_stanzas_W/Westlaw) — OCLC
- [Westlaw OnePass REST API](https://www.perameter.com/docs/westlaw-(onepass)-password-authentication-api) — Perameter
- [Westlaw SAML SSO](https://www.ssoeasy.com/westlaw-saml-sso-php/) — SSO Easy
