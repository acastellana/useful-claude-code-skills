# Useful Claude Code Skills

A collection of useful skills for [Claude Code](https://claude.ai/claude-code).

## Installation

Copy the skill folders to your Claude skills directory:

```bash
# Clone the repo
git clone https://github.com/acastellana/useful-claude-code-skills.git

# Copy skills to Claude's skill directory
cp -r useful-claude-code-skills/notify ~/.claude/skills/
```

Or clone directly into your skills folder:

```bash
cd ~/.claude/skills
git clone https://github.com/acastellana/useful-claude-code-skills.git
```

## Available Skills

### notify

Send desktop notifications cross-platform (macOS, Linux, Windows).

**Usage:**
```bash
/notify
```

Or ask Claude naturally: "notify me when the build is done"

**Features:**
- Works on macOS (osascript), Linux (notify-send), and Windows (PowerShell)
- Optional sound alerts
- Optional subtitles

**Manual usage:**
```bash
python3 ~/.claude/skills/notify/scripts/notify.py -t "Title" -m "Message"
python3 ~/.claude/skills/notify/scripts/notify.py -t "Title" -m "Message" --sound
```

**Platform requirements:**
| OS | Method | Requirements |
|----|--------|--------------|
| macOS | osascript | Built-in |
| Linux | notify-send | `libnotify-bin` (apt) or `libnotify` (dnf/pacman) |
| Windows | PowerShell | Built-in (BurntToast optional for modern toasts) |

## Contributing

Feel free to submit PRs with new skills or improvements to existing ones.

## License

MIT
