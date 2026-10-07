#!/usr/bin/env python3
"""Check every shipped manifest and the skill itself. Exit 1 on any failure.

- Every JSON manifest parses.
- Every manifest names the plugin `contrarian`, and every version
  field (top level, `metadata`, and each marketplace entry) agrees. Copilot, Grok
  and Antigravity show the root plugin.json, so a stale one is what users see.
- SKILL.md has frontmatter with only `name` and `description`, the name matches
  its folder, and the frontmatter fits in 1024 characters.
- The subagent at .claude/agents/contrarian.md is named `contrarian`, and the
  skill body ends with the agent's body word for word, so the two never drift.
- Every Python file in the repo compiles.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "contrarian"
SKILL_DIR = ROOT / "skills" / NAME
AGENT = ROOT / ".claude" / "agents" / f"{NAME}.md"
JSON_MANIFESTS = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".cursor-plugin/marketplace.json",
    ".devin-plugin/plugin.json",
    ".github/plugin/marketplace.json",
    ".grok-plugin/marketplace.json",
    ".kimi-plugin/plugin.json",
    ".muse-plugin/plugin.json",
    "gemini-extension.json",
    "package.json",
    "plugin.json",
]
YAML_MANIFESTS: list[str] = []

errors: list[str] = []
versions: dict[str, str] = {}


def note_version(where: str, value) -> None:
    if value is not None:
        versions[where] = str(value)


for rel in JSON_MANIFESTS:
    path = ROOT / rel
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{rel}: {exc}")
        continue
    if data.get("name") != NAME:
        errors.append(f"{rel}: name is {data.get('name')!r}, expected {NAME!r}")
    note_version(rel, data.get("version"))
    note_version(f"{rel} metadata", (data.get("metadata") or {}).get("version"))
    for entry in data.get("plugins", []):
        if entry.get("name") != NAME:
            errors.append(f"{rel}: plugin entry named {entry.get('name')!r}")
        note_version(f"{rel} plugins[{entry.get('name')}]", entry.get("version"))

for rel in YAML_MANIFESTS:
    text = (ROOT / rel).read_text(encoding="utf-8")
    name = re.search(r"^name:\s*(\S+)", text, re.M)
    if not name or name.group(1) != NAME:
        errors.append(f"{rel}: name does not match {NAME!r}")
    version = re.search(r"^version:\s*(\S+)", text, re.M)
    note_version(rel, version and version.group(1))

if len(set(versions.values())) > 1:
    listing = "\n  ".join(f"{v}  {k}" for k, v in sorted(versions.items()))
    errors.append(f"manifests disagree on version:\n  {listing}")

skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
if not match:
    errors.append("SKILL.md: no frontmatter")
else:
    keys = [line.split(":", 1)[0] for line in match.group(1).splitlines() if re.match(r"^\w", line)]
    if keys != ["name", "description"]:
        errors.append(f"SKILL.md: frontmatter keys must be name, description; found {keys}")
    if not re.search(rf"^name:\s*{NAME}\s*$", match.group(1), re.M):
        errors.append("SKILL.md: name does not match its folder")
    if len(match.group(1)) > 1024:
        errors.append("SKILL.md: frontmatter is over 1024 characters")

agent = AGENT.read_text(encoding="utf-8")
agent_match = re.match(r"^---\n(.*?)\n---\n", agent, re.S)
if not agent_match:
    errors.append(f"{AGENT.relative_to(ROOT)}: no frontmatter")
else:
    if not re.search(rf"^name:\s*{NAME}\s*$", agent_match.group(1), re.M):
        errors.append(f"{AGENT.relative_to(ROOT)}: name is not {NAME!r}")
    if match and not skill[match.end():].endswith(agent[agent_match.end():]):
        errors.append(f"SKILL.md: body does not end with the body of {AGENT.relative_to(ROOT)}; copy the agent's text over")

for script in ROOT.rglob("*.py"):
    if ".git" in script.parts:
        continue
    try:
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    except SyntaxError as exc:
        errors.append(f"{script.relative_to(ROOT)}: does not compile ({exc})")

for e in errors:
    print(f"error: {e}")
print("ok" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
