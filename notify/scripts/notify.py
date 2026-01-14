#!/usr/bin/env python3
"""Send desktop notifications cross-platform (macOS, Linux, Windows)."""

import subprocess
import argparse
import sys
import platform


def send_notification_macos(title: str, message: str, sound: bool = False, subtitle: str = None) -> bool:
    """Send notification on macOS using osascript."""
    title = title.replace('"', '\\"')
    message = message.replace('"', '\\"')

    script = f'display notification "{message}" with title "{title}"'

    if subtitle:
        subtitle = subtitle.replace('"', '\\"')
        script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'

    if sound:
        script += ' sound name "default"'

    try:
        subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def send_notification_linux(title: str, message: str, sound: bool = False, subtitle: str = None) -> bool:
    """Send notification on Linux using notify-send."""
    full_message = f"{subtitle}\n{message}" if subtitle else message

    cmd = ['notify-send', title, full_message]

    try:
        subprocess.run(cmd, check=True, capture_output=True)

        # Play sound if requested (using paplay or aplay)
        if sound:
            for player in ['paplay', 'aplay']:
                sound_files = [
                    '/usr/share/sounds/freedesktop/stereo/complete.oga',
                    '/usr/share/sounds/freedesktop/stereo/message.oga',
                    '/usr/share/sounds/gnome/default/alerts/drip.ogg',
                ]
                for sound_file in sound_files:
                    try:
                        subprocess.run([player, sound_file], check=True, capture_output=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    continue
                break

        return True
    except FileNotFoundError:
        print("notify-send not found. Install libnotify-bin (Debian/Ubuntu) or libnotify (Fedora/Arch)", file=sys.stderr)
        return False
    except subprocess.CalledProcessError:
        return False


def send_notification_windows(title: str, message: str, sound: bool = False, subtitle: str = None) -> bool:
    """Send notification on Windows using PowerShell."""
    full_message = f"{subtitle}: {message}" if subtitle else message

    # Escape single quotes for PowerShell
    title = title.replace("'", "''")
    full_message = full_message.replace("'", "''")

    # Using BurntToast if available, fallback to basic Windows notification
    ps_script = f'''
    $ErrorActionPreference = 'SilentlyContinue'

    # Try BurntToast first
    if (Get-Command New-BurntToastNotification -ErrorAction SilentlyContinue) {{
        New-BurntToastNotification -Text '{title}', '{full_message}'
    }} else {{
        # Fallback to Windows Forms
        Add-Type -AssemblyName System.Windows.Forms
        $balloon = New-Object System.Windows.Forms.NotifyIcon
        $balloon.Icon = [System.Drawing.SystemIcons]::Information
        $balloon.BalloonTipTitle = '{title}'
        $balloon.BalloonTipText = '{full_message}'
        $balloon.Visible = $true
        $balloon.ShowBalloonTip(5000)
        Start-Sleep -Seconds 1
        $balloon.Dispose()
    }}
    '''

    try:
        subprocess.run(
            ['powershell', '-Command', ps_script],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def send_notification(title: str, message: str, sound: bool = False, subtitle: str = None) -> bool:
    """Send a desktop notification (auto-detects OS)."""
    system = platform.system()

    if system == 'Darwin':
        return send_notification_macos(title, message, sound, subtitle)
    elif system == 'Linux':
        return send_notification_linux(title, message, sound, subtitle)
    elif system == 'Windows':
        return send_notification_windows(title, message, sound, subtitle)
    else:
        print(f"Unsupported OS: {system}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Send desktop notifications (cross-platform)")
    parser.add_argument("--title", "-t", required=True, help="Notification title")
    parser.add_argument("--message", "-m", required=True, help="Notification message")
    parser.add_argument("--subtitle", "-s", help="Optional subtitle (macOS/Windows)")
    parser.add_argument("--sound", action="store_true", help="Play notification sound")

    args = parser.parse_args()

    success = send_notification(
        title=args.title,
        message=args.message,
        sound=args.sound,
        subtitle=args.subtitle
    )

    if success:
        print(f"Notification sent: {args.title}")
    else:
        print("Failed to send notification", file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
