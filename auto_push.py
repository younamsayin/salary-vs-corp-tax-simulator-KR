#!/usr/bin/env python3
"""
Auto Git Push Watcher
Watches the project folder and automatically commits + pushes when files change.
"""

import os
import time
import subprocess
import sys
from datetime import datetime

WATCH_DIR = os.path.dirname(os.path.abspath(__file__))
DEBOUNCE_SECONDS = 5  # Wait 5s after last change before committing
IGNORE = {".git", "__pycache__", ".DS_Store", "auto_push.py"}

def get_snapshot(directory):
    """Return a dict of {filepath: mtime} for all tracked files."""
    snapshot = {}
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE]
        for f in files:
            if f in IGNORE or f.endswith(".pyc"):
                continue
            path = os.path.join(root, f)
            try:
                snapshot[path] = os.path.getmtime(path)
            except OSError:
                pass
    return snapshot

def run(cmd):
    result = subprocess.run(cmd, cwd=WATCH_DIR, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def git_push():
    # Check if there's anything to commit
    code, out, _ = run(["git", "status", "--porcelain"])
    if not out:
        return  # Nothing changed

    # Get list of changed files for the commit message
    changed = [line[3:] for line in out.splitlines()]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"Auto-save {timestamp}: {', '.join(changed[:3])}"
    if len(changed) > 3:
        message += f" (+{len(changed) - 3} more)"

    run(["git", "add", "."])
    code, out, err = run(["git", "commit", "-m", message])
    if code != 0:
        print(f"  ⚠️  Commit failed: {err}")
        return

    code, out, err = run(["git", "push"])
    if code == 0:
        print(f"  ✅ Pushed: {message}")
    else:
        print(f"  ❌ Push failed: {err}")

def main():
    print(f"👀 Watching for changes in:")
    print(f"   {WATCH_DIR}")
    print(f"   (auto-pushes {DEBOUNCE_SECONDS}s after you save a file)\n")
    print("   Press Ctrl+C to stop.\n")

    snapshot = get_snapshot(WATCH_DIR)
    last_change_time = None

    while True:
        time.sleep(1)
        current = get_snapshot(WATCH_DIR)

        if current != snapshot:
            snapshot = current
            last_change_time = time.time()
            print(f"  📝 Change detected — waiting {DEBOUNCE_SECONDS}s...")

        # Debounce: push only after no changes for DEBOUNCE_SECONDS
        if last_change_time and (time.time() - last_change_time >= DEBOUNCE_SECONDS):
            last_change_time = None
            git_push()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Watcher stopped.")
        sys.exit(0)
