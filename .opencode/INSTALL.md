# Installing contrarian for OpenCode

This repository ships one skill. OpenCode finds skills on its own in
`~/.config/opencode/skills/<name>/SKILL.md`, so no plugin or config entry is needed.

## Install

Clone the repository and link the skill folder into OpenCode's global skills directory:

```bash
git clone https://github.com/aaddrick/contrarian.git ~/.local/share/contrarian
mkdir -p ~/.config/opencode/skills
ln -s ~/.local/share/contrarian/skills/contrarian ~/.config/opencode/skills/contrarian
```

On Windows, or anywhere symlinks are awkward, copy the folder instead of linking it:

```bash
cp -r ~/.local/share/contrarian/skills/contrarian ~/.config/opencode/skills/
```

To install for one project only, put the folder in that project's `.opencode/skills/` instead.

## Check it installed

```bash
opencode debug skill | grep '"name": "contrarian"'
```

Restart OpenCode. It loads the skill when the task matches. To load it by hand, ask:

```
use the skill tool to load contrarian
```

## Update

```bash
git -C ~/.local/share/contrarian pull
```

If you copied the folder, copy it again after pulling.

## Uninstall

Delete the `contrarian` link (or copied folder) from `~/.config/opencode/skills/`,
then delete the clone at `~/.local/share/contrarian`.
