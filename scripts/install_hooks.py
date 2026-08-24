#!/usr/bin/env python
"""
Helper to install Git post-commit hooks across all active project repositories.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DESKTOP = r"C:\Users\naman\OneDrive\Desktop"
SYNC_SCRIPT = r"C:/Users/naman/OneDrive/Desktop/FundersAI/scripts/sync_resumes.py"

REPOS = [
    os.path.join(DESKTOP, "FundersAI"),
    os.path.join(DESKTOP, "ALLThingsAgentic"),
    os.path.join(DESKTOP, "CareFlow Intelligence"),
]

HOOK_CONTENT = f"""#!/bin/sh
# Auto-sync resume statistics after commit
python "{SYNC_SCRIPT}" || true
"""

def install_hooks():
    print("=" * 60)
    print("🔧 INSTALLING GIT POST-COMMIT HOOKS")
    print("=" * 60)

    for repo in REPOS:
        hooks_dir = os.path.join(repo, ".git", "hooks")
        if os.path.exists(hooks_dir):
            hook_path = os.path.join(hooks_dir, "post-commit")
            with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(HOOK_CONTENT)
            print(f"  ✓ Installed post-commit hook: {repo}")
        else:
            print(f"  ⚠ Skipped (no .git directory): {repo}")

    print("\n✅ All Git post-commit hooks successfully installed!")

if __name__ == "__main__":
    install_hooks()
