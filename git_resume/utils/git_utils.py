import os
import subprocess
from typing import Dict, List, Any

def get_git_stats(repo_path: str) -> Dict[str, Any]:
    if not os.path.exists(repo_path):
        return {"commits": 0, "files": 0, "loc": 0, "test_suites": 0}

    stats = {}
    
    # 1. Total commits
    try:
        commits = subprocess.check_output(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        stats["commits"] = int(commits)
    except Exception:
        stats["commits"] = 0

    # 2. Tracked code files and lines of code
    try:
        files = subprocess.check_output(
            ["git", "ls-files"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL
        ).splitlines()

        code_exts = {".py", ".ts", ".tsx", ".js", ".mjs", ".sql", ".html", ".css", ".md"}
        code_files = [f for f in files if any(f.endswith(ext) for ext in code_exts)]
        
        total_loc = 0
        for cf in code_files:
            p = os.path.join(repo_path, cf)
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                        total_loc += sum(1 for _ in fp)
                except Exception:
                    pass

        stats["files"] = len(code_files)
        stats["loc"] = total_loc

        # 3. Test suites
        test_files = [
            f for f in files
            if ("test_" in os.path.basename(f) or f.endswith(".test.ts") or f.endswith(".test.tsx") or f.endswith(".test.js") or f.endswith(".test.mjs"))
            and not any(x in f for x in ["node_modules", ".venv", ".pytest_cache", ".next"])
        ]
        stats["test_suites"] = len(test_files)
    except Exception:
        stats["files"] = 0
        stats["loc"] = 0
        stats["test_suites"] = 0

    return stats

def get_recent_commits(repo_path: str, count: int = 15) -> List[Dict[str, str]]:
    if not os.path.exists(repo_path):
        return []
    try:
        output = subprocess.check_output(
            ["git", "log", f"-n{count}", "--pretty=format:%h|%an|%s|%cd", "--date=short"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        
        commits = []
        for line in output.splitlines():
            if "|" in line:
                parts = line.split("|", 3)
                commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "message": parts[2],
                    "date": parts[3] if len(parts) > 3 else ""
                })
        return commits
    except Exception:
        return []
