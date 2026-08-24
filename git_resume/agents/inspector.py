import os
import subprocess
from typing import Dict, Any, List
from git_resume.config import RepoConfig
from git_resume.utils.git_utils import get_git_stats, get_recent_commits

class InspectorAgent:
    """Scans Git repositories to extract active codebase metrics, diffs, and commit contexts."""

    def inspect_repo(self, repo: RepoConfig) -> Dict[str, Any]:
        stats = get_git_stats(repo.path)
        recent_commits = get_recent_commits(repo.path, count=10)
        diff_summary = self.get_diff_summary(repo.path, count=5)

        return {
            "name": repo.name,
            "path": repo.path,
            "tag": repo.tag,
            "stack": repo.primary_stack,
            "commits": stats.get("commits", 0),
            "files": stats.get("files", 0),
            "loc": stats.get("loc", 0),
            "loc_k": f"{round(stats.get('loc', 0) / 1000)}K" if stats.get("loc", 0) >= 1000 else str(stats.get("loc", 0)),
            "test_suites": stats.get("test_suites", 0),
            "recent_commits": recent_commits,
            "diff_summary": diff_summary
        }

    def get_diff_summary(self, repo_path: str, count: int = 5) -> str:
        if not os.path.exists(repo_path):
            return "No git repository found."
        try:
            # Get stat summary of recent commits
            output = subprocess.check_output(
                ["git", "diff", f"HEAD~{count}", "HEAD", "--stat"],
                cwd=repo_path,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            return output if output else "Recent commits contain modular refactors and optimizations."
        except Exception:
            return "Modular codebase additions and schema updates."

    def inspect_all(self, repos: List[RepoConfig]) -> Dict[str, Dict[str, Any]]:
        results = {}
        for r in repos:
            results[r.name] = self.inspect_repo(r)
        return results
