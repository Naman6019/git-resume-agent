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

def get_last_commit_touching(repo_path: str, filename: str) -> Optional[str]:
    """Returns the SHA of the most recent commit that touched `filename`, or None
    if the file has no history (or the repo doesn't exist)."""
    if not is_git_repo(repo_path):
        return None
    try:
        sha = subprocess.check_output(
            ["git", "log", "-1", "--format=%H", "--", filename],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return sha or None
    except Exception:
        return None


def get_file_diff(repo_path: str, old_sha: str, new_sha: str, filename: str) -> str:
    """Unified diff of `filename` between two commits. Empty string on any failure."""
    try:
        return subprocess.check_output(
            ["git", "diff", f"{old_sha}..{new_sha}", "--", filename],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return ""


def get_file_at_commit(repo_path: str, sha: str, filename: str) -> str:
    """Content of `filename` as of `sha`. Empty string if it didn't exist there."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{sha}:{filename}"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return ""


def get_commit_message(repo_path: str, sha: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%s", sha],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return ""


def open_portfolio_pr(
    repo_path: str,
    base_branch: str,
    branch_name: str,
    files: List[str],
    commit_message: str,
    pr_title: str,
    pr_body: str,
) -> Dict[str, Any]:
    """Branches off `base_branch`, commits `files`, pushes, and opens a GitHub PR
    via `gh`. Always leaves the repo back on `base_branch` when done, whether or
    not the PR was created, so other tooling (e.g. the resume sync) isn't
    surprised by a dangling feature branch checkout."""
    if not is_git_repo(repo_path):
        return {"success": False, "reason": "not a git repository"}

    try:
        subprocess.check_call(["git", "fetch", "origin", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "checkout", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "pull", "--ff-only", "origin", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "checkout", "-B", branch_name], cwd=repo_path, stderr=subprocess.DEVNULL)
        subprocess.check_call(["git", "add"] + files, cwd=repo_path, stderr=subprocess.DEVNULL)

        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], cwd=repo_path, text=True, stderr=subprocess.DEVNULL
        ).strip()
        if not staged:
            subprocess.check_call(["git", "checkout", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "branch", "-D", branch_name], cwd=repo_path, stderr=subprocess.DEVNULL)
            return {"success": True, "skipped": True, "reason": "no changes to commit"}

        subprocess.check_call(["git", "commit", "-m", commit_message], cwd=repo_path, stderr=subprocess.DEVNULL)
        push = subprocess.run(
            ["git", "push", "-u", "origin", branch_name, "--force-with-lease"],
            cwd=repo_path, text=True, capture_output=True,
        )
        if push.returncode != 0:
            subprocess.check_call(["git", "checkout", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
            return {"success": False, "reason": f"push failed: {push.stderr.strip() or push.stdout.strip()}"}

        pr = subprocess.run(
            ["gh", "pr", "create", "--base", base_branch, "--head", branch_name, "--title", pr_title, "--body", pr_body],
            cwd=repo_path, text=True, capture_output=True,
        )
        subprocess.check_call(["git", "checkout", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)

        if pr.returncode != 0:
            return {"success": False, "reason": f"gh pr create failed: {pr.stderr.strip() or pr.stdout.strip()}", "branch": branch_name}

        pr_url = pr.stdout.strip().splitlines()[-1] if pr.stdout.strip() else ""
        return {"success": True, "skipped": False, "pr_url": pr_url, "branch": branch_name}
    except subprocess.CalledProcessError as e:
        try:
            subprocess.check_call(["git", "checkout", base_branch], cwd=repo_path, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        return {"success": False, "reason": str(e)}


def commit_and_push(repo_path: str, message: str, paths: Optional[List[str]] = None) -> Dict[str, Any]:
    """Stages, commits, and pushes changes in repo_path. Safe to call with nothing to commit."""
    if not is_git_repo(repo_path):
        return {"success": False, "skipped": True, "reason": "not a git repository"}

    try:
        subprocess.check_call(
            ["git", "add"] + (paths if paths else ["-A"]),
            cwd=repo_path,
            stderr=subprocess.DEVNULL,
        )

        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if not staged:
            return {"success": True, "skipped": True, "reason": "no changes to commit"}

        subprocess.check_call(
            ["git", "commit", "-m", message],
            cwd=repo_path,
            stderr=subprocess.DEVNULL,
        )

        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()

        push = subprocess.run(
            ["git", "push", "origin", branch],
            cwd=repo_path,
            text=True,
            capture_output=True,
        )
        if push.returncode != 0:
            return {
                "success": False,
                "skipped": False,
                "reason": f"push failed: {push.stderr.strip() or push.stdout.strip()}",
                "files": staged.splitlines(),
                "branch": branch,
            }

        return {"success": True, "skipped": False, "files": staged.splitlines(), "branch": branch}
    except subprocess.CalledProcessError as e:
        return {"success": False, "skipped": False, "reason": str(e)}


def get_git_config(key: str, repo_path: Optional[str] = None) -> Optional[str]:
    """Retrieves a local or global git config value."""
    cmd = ["git", "config", "--get", key]
    cwd = repo_path if repo_path and os.path.exists(repo_path) else None
    try:
        res = subprocess.check_output(cmd, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
        return res if res else None
    except Exception:
        return None

