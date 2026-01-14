---
name: notify
description: Send desktop notifications to alert the user. Works on macOS, Linux, and Windows. Use when tasks complete, builds finish, tests pass/fail, or any time the user needs to be notified.
user-invocable: true
---

# Desktop Notifications (Cross-Platform)

Send desktop notifications to alert the user. Automatically detects the OS and uses the appropriate method.

## Instructions

Use the bundled Python script:

```bash
python3 ~/.claude/skills/notify/scripts/notify.py --title "Title" --message "Message"
```

With sound:
```bash
python3 ~/.claude/skills/notify/scripts/notify.py --title "Title" --message "Message" --sound
```

With subtitle (macOS/Windows):
```bash
python3 ~/.claude/skills/notify/scripts/notify.py --title "Title" --message "Message" --subtitle "Subtitle"
```

## Platform Support

| OS | Method | Requirements |
|----|--------|--------------|
| macOS | osascript | Built-in |
| Linux | notify-send | `libnotify-bin` (apt) or `libnotify` (dnf/pacman) |
| Windows | PowerShell + Windows Forms | Built-in (BurntToast optional) |

## When to use

- After long-running tasks complete (builds, tests, deployments)
- When errors occur that need user attention
- When user explicitly asks to be notified
- After completing a series of tasks

## Examples

**Task complete:**
```bash
python3 ~/.claude/skills/notify/scripts/notify.py -t "Task Complete" -m "All files have been processed"
```

**Build finished:**
```bash
python3 ~/.claude/skills/notify/scripts/notify.py -t "Build Complete" -m "Build finished successfully" --sound
```

**Test results:**
```bash
python3 ~/.claude/skills/notify/scripts/notify.py -t "Tests Passed" -m "All 50 tests passed"
```

**Error alert:**
```bash
python3 ~/.claude/skills/notify/scripts/notify.py -t "Build Failed" -m "3 TypeScript errors" --sound
```

## Best practices

- Keep titles short (under 30 characters)
- Messages can be longer but stay concise
- Use sound for important notifications only
- Include relevant details (counts, times, status)
