# Contributing

Corrections, new anti-patterns, and sharper techniques are welcome.

## Change the agent

The text lives in two places:

- `.claude/agents/contrarian.md` is the subagent, and the source.
- `skills/contrarian/SKILL.md` is the skill every other harness loads. Its body is a one-line note about running in a subagent, followed by the agent's body word for word.

Edit the agent first, then copy everything below its frontmatter over the matching part of `SKILL.md`. `scripts/check_configs.py` fails if the two differ.

A good change comes from a proposal you saw it handle badly:

- what the proposal was and what the contrarian said,
- what it should have said, and which part of the prompt would have led it there,
- the model, if the behaviour is model-specific.

Keep the skill's frontmatter short. Every harness loads its description at the start of each session, and the frontmatter must stay under 1024 characters. Don't use `: ` inside the description; some harnesses parse it as YAML.

## Change a manifest

Each harness reads its own file. Every manifest must carry the same name and version:

| Harness | Files |
|---|---|
| Claude Code, Claude Desktop, Cowork, claude.ai | `.claude-plugin/plugin.json` (also points at the subagent), `.claude-plugin/marketplace.json` |
| Codex | `.codex-plugin/plugin.json` (marketplace from `.claude-plugin/`) |
| Antigravity CLI, and the plugin manifest Copilot CLI and Grok read | `plugin.json` |
| Cursor | `.cursor-plugin/plugin.json`, `.cursor-plugin/marketplace.json` |
| Devin CLI | `.devin-plugin/plugin.json` |
| Factory Droid | reads `.claude-plugin/` |
| Gemini CLI | `gemini-extension.json` |
| GitHub Copilot CLI | `.github/plugin/marketplace.json` |
| Grok Build CLI | `.grok-plugin/marketplace.json` |
| Hermes Agent | `plugin.json` |
| Kimi Code | `.kimi-plugin/plugin.json` |
| Muse Code | `.muse-plugin/plugin.json` |
| Muse (muse.ai) | `scripts/install_muse.sh` |
| OpenCode | `.opencode/INSTALL.md` (no manifest; OpenCode finds the skill folder) |
| Pi | `package.json` (`pi` key) |

To release a new version, bump `version` in every file above. `scripts/check_configs.py` fails if any of them disagree.

Some harnesses read files meant for others. Copilot and Grok take the root `plugin.json` ahead of `.claude-plugin/plugin.json`. Hermes scans the whole repository before it installs. If you add a file for one harness, run the plugin-load workflow so every other harness gets checked too.

## Before you open a pull request

```bash
python3 scripts/check_configs.py
python3 -m unittest discover -s tests -v
```

The `plugin loads` workflow installs the plugin into a scratch config for each harness and checks that it finds the skill. It runs on pull requests that touch a manifest, the skill, or the agent.

## Social preview

`scripts/make_card.py` renders `.github/assets/social-preview.png` with Pillow, in the poster's palette and fonts. GitHub reads the preview only from **Settings > General > Social preview**, so upload the new PNG there by hand after you regenerate it.
