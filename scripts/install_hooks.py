#!/usr/bin/env python
"""
Helper to install Git post-commit hooks across all repositories configured in gitresume.yaml.
"""

import os
import sys
from git_resume.config import load_config

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def install_hooks(config_path: str = "gitresume.yaml"):
    config = load_config(config_path)

    print("=" * 60)
    print("🔧 INSTALLING GIT POST-COMMIT HOOKS FROM gitresume.yaml")
    print("=" * 60)

    hook_content = """#!/bin/sh
# GitResume AI: Auto-sync resume statistics after commit
git-resume sync || python -m git_resume.cli sync || true
"""

    installed_count = 0
    for repo in config.repositories:
        repo_path = repo.path
        git_dir = os.path.join(repo_path, ".git")
        hooks_dir = os.path.join(git_dir, "hooks")

        if os.path.exists(git_dir):
            os.makedirs(hooks_dir, exist_ok=True)
            hook_path = os.path.join(hooks_dir, "post-commit")
            
            with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(hook_content)

            # Make executable on Unix / WSL if applicable
            try:
                os.chmod(hook_path, 0o755)
            except Exception:
                pass

            print(f"  ✓ Installed hook for [{repo.name}]: {repo_path}")
            installed_count += 1
        else:
            print(f"  ⚠ Skipped [{repo.name}] (no .git directory found at {repo_path})")

    print(f"\n✅ Successfully installed post-commit hooks across {installed_count} repositories!")

if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "gitresume.yaml"
    install_hooks(cfg)
