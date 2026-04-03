#!/usr/bin/env python3
"""
Auto Git Push Watcher
Watches the project folder and automatically commits + pushes when files change.
"""

import time
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WATCH_DIR = Path(__file__).resolve().parent
DEBOUNCE_SECONDS = 5  # Wait 5s after last change before committing
IGNORE_DIRS  = {".git", "__pycache__"}
IGNORE_FILES = {".DS_Store", "auto_push.py"}


def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, cwd=cwd or WATCH_DIR, capture_output=True, text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_git():
    """Exit with a friendly message if git is not installed."""
    code, _, err = run(["git", "--version"])
    if code != 0:
        print(f"❌ git not found: {err}")
        sys.exit(1)


def get_snapshot(directory):
    """Return a dict of {Path: mtime} for all tracked files."""
    snapshot = {}
    for path in directory.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.name in IGNORE_FILES:
            continue
        if path.is_file():
            try:
                snapshot[path] = path.stat().st_mtime
            except OSError:
                pass
    return snapshot


def git_push():
    # Let git be the single source of truth for what changed
    code, out, err = run(["git", "status", "--porcelain"])
    if code != 0:
        print(f"  ⚠️  git status failed: {err}")
        return
    if not out:
        return  # Nothing to commit

    # Build commit message — handle renames and quoted paths
    changed = []
    for line in out.splitlines():
        filename = line[3:]
        if " -> " in filename:          # renamed: show the new name only
            filename = filename.split(" -> ")[-1]
        changed.append(filename.strip('"'))

    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    message = f"Auto-save {timestamp}: {', '.join(changed[:3])}"
    if len(changed) > 3:
        message += f" (+{len(changed) - 3} more)"

    code, _, err = run(["git", "add", "."])
    if code != 0:
        print(f"  ⚠️  git add failed: {err}")
        return

    code, _, err = run(["git", "commit", "-m", message])
    if code != 0:
        print(f"  ⚠️  Commit failed: {err}")
        return

    code, _, err = run(["git", "push"])
    if code == 0:
        print(f"  ✅ Pushed: {message}")
    else:
        print(f"  ❌ Push failed: {err}")


def main():
    check_git()
    print(f"👀 Watching for changes in:")
    print(f"   {WATCH_DIR}")
    print(f"   (auto-pushes {DEBOUNCE_SECONDS}s after you save a file)\n")
    print("   Press Ctrl+C to stop.\n")

    snapshot = get_snapshot(WATCH_DIR)
    last_change_time = None

    while True:
        time.sleep(1)

        if last_change_time is None:
            # Only scan the directory when not already in the debounce window
            current = get_snapshot(WATCH_DIR)
            if current != snapshot:
                snapshot = current
                last_change_time = time.time()
                print(f"  📝 Change detected — waiting {DEBOUNCE_SECONDS}s...")

        elif time.time() - last_change_time >= DEBOUNCE_SECONDS:
            last_change_time = None
            git_push()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Watcher stopped.")
