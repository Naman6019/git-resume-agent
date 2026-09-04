import os
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple

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

def get_git_remote_url(repo_path: str) -> Optional[str]:
    """Retrieves and normalizes the git origin remote URL into clean HTTPS format."""
    if not os.path.exists(repo_path):
        return None
    try:
        remote = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        if not remote:
            return None
        
        # Convert SSH (git@github.com:user/repo.git) to HTTPS (https://github.com/user/repo)
        if remote.startswith("git@github.com:"):
            path_part = remote[len("git@github.com:"):]
            remote = f"https://github.com/{path_part}"
        elif remote.startswith("git@"):
            # Generic git@host:path
            parts = remote.split("@", 1)[1].split(":", 1)
            if len(parts) == 2:
                remote = f"https://{parts[0]}/{parts[1]}"
        
        if remote.endswith(".git"):
            remote = remote[:-4]
            
        return remote
    except Exception:
        return None

def is_git_repo(repo_path: str) -> bool:
    """Checks if a directory is an initialized Git repository."""
    if not repo_path or not os.path.exists(repo_path):
        return False
    git_dir = os.path.join(repo_path, ".git")
    if os.path.exists(git_dir):
        return True
    try:
        res = subprocess.check_output(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        return res == "true"
    except Exception:
        return False

def get_git_remote_details(repo_path: str) -> Dict[str, Any]:
    """Inspects Git remote information, detecting GitHub repositories."""
    if not is_git_repo(repo_path):
        return {
            "is_git": False,
            "has_remote": False,
            "remote_url": None,
            "is_github": False,
            "repo_identifier": None
        }
    
    remote_url = get_git_remote_url(repo_path)
    if not remote_url:
        return {
            "is_git": True,
            "has_remote": False,
            "remote_url": None,
            "is_github": False,
            "repo_identifier": None
        }
    
    is_github = "github.com" in remote_url.lower()
    repo_identifier = None
    if is_github:
        match = re.search(r'github\.com[/:]([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', remote_url)
        if match:
            repo_identifier = match.group(1).rstrip(".git")

    return {
        "is_git": True,
        "has_remote": True,
        "remote_url": remote_url,
        "is_github": is_github,
        "repo_identifier": repo_identifier
    }

def set_git_config(repo_path: str, key: str, value: str) -> bool:
    """Sets a repository-local git config key-value pair."""
    if not is_git_repo(repo_path):
        return False
    try:
        subprocess.check_call(
            ["git", "config", key, value],
            cwd=repo_path,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception:
        return False

def get_git_config(key: str, repo_path: Optional[str] = None) -> Optional[str]:
    """Retrieves a local or global git config value."""
    cmd = ["git", "config", "--get", key]
    cwd = repo_path if repo_path and os.path.exists(repo_path) else None
    try:
        res = subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
        return res if res else None
    except Exception:
        return None

