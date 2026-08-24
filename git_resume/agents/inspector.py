from typing import Dict, Any, List
from git_resume.config import RepoConfig
from git_resume.utils.git_utils import get_git_stats, get_recent_commits

class InspectorAgent:
    """Scans Git repositories to extract active codebase metrics and commit diffs."""

    def inspect_repo(self, repo: RepoConfig) -> Dict[str, Any]:
        stats = get_git_stats(repo.path)
        recent_commits = get_recent_commits(repo.path, count=10)

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
            "recent_commits": recent_commits
        }

    def inspect_all(self, repos: List[RepoConfig]) -> Dict[str, Dict[str, Any]]:
        results = {}
        for r in repos:
            results[r.name] = self.inspect_repo(r)
        return results
