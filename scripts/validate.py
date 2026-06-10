#!/usr/bin/env python3
"""Validate the Legal Engineering plugin structure.

Checks:
1. All JSON files parse correctly
2. All SKILL.md files have required YAML frontmatter (name, description)
3. All agent .md files have required YAML frontmatter (name, description)
4. marketplace.json and plugin.json name/description consistency
5. Skill directory names match SKILL.md frontmatter names
6. registry.json lists match actual files on disk
7. Count verification across registry, marketplace, and plugins
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIRS = {
    "cross-border-wealth": REPO_ROOT / "cross-border-wealth",
    "legal-pathways": REPO_ROOT / "legal-pathways",
}
errors: list[str] = []
warnings: list[str] = []


def check_json_files():
    for f in REPO_ROOT.rglob("*.json"):
        try:
            json.loads(f.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"JSON parse error in {f.relative_to(REPO_ROOT)}: {e}")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip()
    return fm


def check_skills(plugin_name: str, plugin_dir: Path):
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        errors.append(f"{plugin_name}: skills/ directory missing")
        return
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{plugin_name}: Missing SKILL.md in skills/{skill_dir.name}/")
            continue
        fm = parse_frontmatter(skill_md.read_text())
        if fm is None:
            errors.append(
                f"{plugin_name}: No YAML frontmatter in {skill_md.relative_to(REPO_ROOT)}"
            )
            continue
        if "description" not in fm:
            errors.append(
                f"{plugin_name}: Missing 'description' in {skill_md.relative_to(REPO_ROOT)} frontmatter"
            )
        if "version" not in fm:
            warnings.append(
                f"{plugin_name}: Missing 'version' in {skill_md.relative_to(REPO_ROOT)} frontmatter"
            )
        fm_name = fm.get("name", "")
        if fm_name and fm_name != skill_dir.name:
            errors.append(
                f"{plugin_name}: Skill name mismatch: directory '{skill_dir.name}' vs frontmatter name '{fm_name}'"
            )


def check_agents(plugin_name: str, plugin_dir: Path):
    agents_dir = plugin_dir / "agents"
    if not agents_dir.exists():
        warnings.append(f"{plugin_name}: agents/ directory missing (optional)")
        return
    for agent_md in sorted(agents_dir.glob("*.md")):
        fm = parse_frontmatter(agent_md.read_text())
        if fm is None:
            errors.append(
                f"{plugin_name}: No YAML frontmatter in {agent_md.relative_to(REPO_ROOT)}"
            )
            continue
        if "name" not in fm:
            errors.append(
                f"{plugin_name}: Missing 'name' in {agent_md.relative_to(REPO_ROOT)} frontmatter"
            )
        if "description" not in fm:
            errors.append(
                f"{plugin_name}: Missing 'description' in {agent_md.relative_to(REPO_ROOT)} frontmatter"
            )


def check_manifests():
    mp_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    if not mp_path.exists():
        errors.append("Missing .claude-plugin/marketplace.json")
        return
    mp = json.loads(mp_path.read_text())
    if not mp.get("plugins"):
        errors.append("marketplace.json has no plugins array")
        return

    for mp_plugin in mp["plugins"]:
        plugin_name = mp_plugin.get("name", "unknown")
        pp_path = REPO_ROOT / plugin_name / ".claude-plugin" / "plugin.json"
        if not pp_path.exists():
            errors.append(f"Missing {plugin_name}/.claude-plugin/plugin.json")
            continue
        pp = json.loads(pp_path.read_text())
        if mp_plugin.get("name") != pp.get("name"):
            errors.append(
                f"Name mismatch: marketplace '{mp_plugin.get('name')}' vs plugin '{pp.get('name')}'"
            )
        if mp_plugin.get("description") != pp.get("description"):
            warnings.append(
                f"Description differs between marketplace.json and {plugin_name}/plugin.json"
            )


def check_registry():
    """Validate registry.json against actual files on disk."""
    reg_path = REPO_ROOT / "registry.json"
    if not reg_path.exists():
        errors.append("Missing registry.json")
        return
    reg = json.loads(reg_path.read_text())

    # --- Skill validation ---
    registry_skills: dict[str, list[str]] = {}
    for skill in reg.get("skills", []):
        plugin = skill.get("plugin", "unknown")
        registry_skills.setdefault(plugin, []).append(skill["name"])
        # Check that the path exists
        skill_path = REPO_ROOT / skill.get("path", "")
        if not skill_path.exists():
            errors.append(
                f"Registry skill '{skill['name']}' in '{plugin}' points to missing file: {skill['path']}"
            )

    for plugin_name, plugin_dir in PLUGIN_DIRS.items():
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            continue
        disk_skills = sorted(
            d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
        )
        reg_skill_names = sorted(registry_skills.get(plugin_name, []))
        for s in disk_skills:
            if s not in reg_skill_names:
                errors.append(
                    f"Skill '{s}' exists on disk in {plugin_name}/skills/ but is missing from registry.json"
                )
        for s in reg_skill_names:
            if s not in disk_skills:
                errors.append(
                    f"Skill '{s}' listed in registry.json for {plugin_name} but not found on disk"
                )

    # --- Agent validation ---
    registry_agents: dict[str, list[str]] = {}
    for agent in reg.get("agents", []):
        plugin = agent.get("plugin", "unknown")
        registry_agents.setdefault(plugin, []).append(agent["name"])
        agent_path = REPO_ROOT / agent.get("path", "")
        if not agent_path.exists():
            errors.append(
                f"Registry agent '{agent['name']}' in '{plugin}' points to missing file: {agent['path']}"
            )

    for plugin_name, plugin_dir in PLUGIN_DIRS.items():
        agents_dir = plugin_dir / "agents"
        if not agents_dir.exists():
            continue
        disk_agents = sorted(a.stem for a in agents_dir.glob("*.md"))
        reg_agent_names = sorted(registry_agents.get(plugin_name, []))
        for a in disk_agents:
            if a not in reg_agent_names:
                errors.append(
                    f"Agent '{a}' exists on disk in {plugin_name}/agents/ but is missing from registry.json"
                )
        for a in reg_agent_names:
            if a not in disk_agents:
                errors.append(
                    f"Agent '{a}' listed in registry.json for {plugin_name} but not found on disk"
                )

    # --- Reference validation ---
    registry_refs: dict[str, list[str]] = {}
    for ref in reg.get("references", []):
        plugin = ref.get("plugin", "unknown")
        registry_refs.setdefault(plugin, []).append(ref["name"])
        ref_path = REPO_ROOT / ref.get("path", "")
        if not ref_path.exists():
            errors.append(
                f"Registry reference '{ref['name']}' in '{plugin}' points to missing file: {ref['path']}"
            )

    for plugin_name, plugin_dir in PLUGIN_DIRS.items():
        refs_dir = plugin_dir / "references"
        if not refs_dir.exists():
            continue
        disk_refs = sorted(r.stem for r in refs_dir.iterdir() if r.is_file())
        reg_ref_names = sorted(registry_refs.get(plugin_name, []))
        for r in disk_refs:
            if r not in reg_ref_names:
                errors.append(
                    f"Reference '{r}' exists on disk in {plugin_name}/references/ but is missing from registry.json"
                )
        for r in reg_ref_names:
            if r not in disk_refs:
                errors.append(
                    f"Reference '{r}' listed in registry.json for {plugin_name} but not found on disk"
                )


def check_counts():
    """Verify counts in registry.json and marketplace.json are accurate."""
    reg_path = REPO_ROOT / "registry.json"
    mp_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"

    if not reg_path.exists() or not mp_path.exists():
        return

    reg = json.loads(reg_path.read_text())
    mp = json.loads(mp_path.read_text())

    # Count actual skills per plugin in registry
    skill_counts: dict[str, int] = {}
    for skill in reg.get("skills", []):
        plugin = skill.get("plugin", "unknown")
        skill_counts[plugin] = skill_counts.get(plugin, 0) + 1

    total_skills = sum(skill_counts.values())
    declared_total = reg.get("total", 0)
    if total_skills != declared_total:
        errors.append(
            f"registry.json 'total' is {declared_total} but actual skill count is {total_skills}"
        )

    declared_plugins = reg.get("plugins", {})
    for plugin_name, declared_count in declared_plugins.items():
        actual = skill_counts.get(plugin_name, 0)
        if actual != declared_count:
            errors.append(
                f"registry.json plugins.{plugin_name} declares {declared_count} skills but has {actual}"
            )

    # Count actual agents per plugin
    agent_counts: dict[str, int] = {}
    for agent in reg.get("agents", []):
        plugin = agent.get("plugin", "unknown")
        agent_counts[plugin] = agent_counts.get(plugin, 0) + 1

    # Count actual references per plugin
    ref_counts: dict[str, int] = {}
    for ref in reg.get("references", []):
        plugin = ref.get("plugin", "unknown")
        ref_counts[plugin] = ref_counts.get(plugin, 0) + 1

    # Verify marketplace.json stats if present
    mp_stats = mp.get("stats", {})
    if mp_stats:
        if mp_stats.get("totalSkills") != total_skills:
            errors.append(
                f"marketplace.json stats.totalSkills is {mp_stats.get('totalSkills')} "
                f"but registry has {total_skills}"
            )
        total_agents = sum(agent_counts.values())
        if mp_stats.get("totalAgents") != total_agents:
            errors.append(
                f"marketplace.json stats.totalAgents is {mp_stats.get('totalAgents')} "
                f"but registry has {total_agents}"
            )
        total_refs = sum(ref_counts.values())
        if mp_stats.get("totalReferences") != total_refs:
            errors.append(
                f"marketplace.json stats.totalReferences is {mp_stats.get('totalReferences')} "
                f"but registry has {total_refs}"
            )

    # Verify marketplace plugin-level counts if present
    for mp_plugin in mp.get("plugins", []):
        pname = mp_plugin.get("name", "")
        if "skills" in mp_plugin:
            actual = skill_counts.get(pname, 0)
            if mp_plugin["skills"] != actual:
                errors.append(
                    f"marketplace.json plugin '{pname}' declares {mp_plugin['skills']} skills "
                    f"but registry has {actual}"
                )
        if "agents" in mp_plugin:
            actual = agent_counts.get(pname, 0)
            if mp_plugin["agents"] != actual:
                errors.append(
                    f"marketplace.json plugin '{pname}' declares {mp_plugin['agents']} agents "
                    f"but registry has {actual}"
                )
        if "references" in mp_plugin:
            actual = ref_counts.get(pname, 0)
            if mp_plugin["references"] != actual:
                errors.append(
                    f"marketplace.json plugin '{pname}' declares {mp_plugin['references']} references "
                    f"but registry has {actual}"
                )


def main():
    check_json_files()

    for plugin_name, plugin_dir in PLUGIN_DIRS.items():
        check_skills(plugin_name, plugin_dir)
        check_agents(plugin_name, plugin_dir)

    check_manifests()
    check_registry()
    check_counts()

    if errors:
        print(f"\n{'='*60}")
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  * {e}")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    if not errors and not warnings:
        print("All checks passed.")
    print()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
