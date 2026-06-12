# Legal-Engineering-Public — CLAUDE.md

> **Standalone / third-party upstream — light treatment.** This is the **public upstream** of the
> legal-engineering plugin. Its reviewed content has already been **integrated into
> `Skill/Zereo-skills/legal-engineering`**, which is the maintained copy used by the Salecraft suite.
> We are **not** pushing or deeply maintaining this repo here; do not document its internals in depth.

## What this repo is
A Claude Code plugin marketplace for legal engineering — cross-border wealth structuring, sovereign
individual architecture, professional/aviation licensing, and immigration pathways. It contains two
plugins (`cross-border-wealth`, `legal-pathways`) and a `westlaw-mcp` server. See its own
`README.md` and the per-plugin docs for details; this file intentionally stays shallow.

## Working here
- **Prefer editing the integrated copy** in `Skill/Zereo-skills/legal-engineering` rather than this
  upstream, unless you are specifically syncing from upstream.
- In the Salecraft suite, legal/compliance review is reached through the **`legal-engineering`
  review gate owned by the Social-Engineering plugin** (`../Social-Engineering/skills/legal-engineering`),
  which is backed by this domain. Route claims/pricing/compliance there.
- The existing `cross-border-wealth/CLAUDE.md` and `legal-pathways/CLAUDE.md` are practice-profile
  **templates** (copied to the user's config on first run), not project context — leave them as-is.

## Repository & development

- **Repo:** [`Zereo0317/legal-engineering-system`](https://github.com/Zereo0317/legal-engineering-system) (**private**). Clone: `git clone https://github.com/Zereo0317/legal-engineering-system.git`.
- **Shape:** a Claude Code **marketplace** (`.claude-plugin/marketplace.json`, `legal-engineering`) of two plugins — `cross-border-wealth` and `legal-pathways` — plus a bundled `westlaw-mcp` server (`pip install -r westlaw-mcp/requirements.txt`).
- **Maintenance (intentionally shallow):** this is the **public upstream**; the maintained copy lives in `Skill/Zereo-skills/legal-engineering`. Don't deep-document internals here, and leave the per-plugin template `CLAUDE.md` files (`cross-border-wealth/`, `legal-pathways/`) as-is.
- **`.gitignore`** excludes secrets, Python caches (`__pycache__/`, `.venv/`), and build artifacts.

## Relevant skills
When working here, reach for these skills in ../../../Skill/Zereo-skills (search registry.json):
- legal-engineering — the maintained, integrated legal skill category (start here).
- 06-knowledge-management — for the references / matter-management material.
Search `Skill/Zereo-skills/registry.json` by keyword (legal, compliance, jurisdiction) for more.
