import os
import re
import json
import yaml
from typing import Dict, Any, List, Tuple, Optional
from git_resume.utils.git_utils import get_git_remote_url
from git_resume.config import find_config_path

TECH_KEYWORDS = [
    ("fastapi", "FastAPI"),
    ("python", "Python"),
    ("react", "React"),
    ("typescript", "TypeScript"),
    ("javascript", "JavaScript"),
    ("next.js", "Next.js"),
    ("nextjs", "Next.js"),
    ("tailwind", "TailwindCSS"),
    ("tailwindcss", "TailwindCSS"),
    ("qdrant", "Qdrant"),
    ("chroma", "ChromaDB"),
    ("chromadb", "ChromaDB"),
    ("postgresql", "PostgreSQL"),
    ("postgres", "PostgreSQL"),
    ("supabase", "Supabase"),
    ("firestore", "Firestore"),
    ("google cloud run", "Google Cloud Run"),
    ("cloud run", "Google Cloud Run"),
    ("langgraph", "LangGraph"),
    ("google adk", "Google ADK"),
    ("vertex ai", "Vertex AI"),
    ("redis", "Redis"),
    ("celery", "Celery"),
    ("vite", "Vite"),
    ("unsloth", "Unsloth"),
    ("ollama", "Ollama"),
    ("docker", "Docker"),
    ("kubernetes", "Kubernetes"),
]

class SchemaDiscoverer:
    """Discovers project tags, tracks, and primary tech stacks from README.md and manifests."""

    def discover_repo_metadata(self, repo_path: str, fallback_name: str = "") -> Dict[str, Any]:
        if not os.path.exists(repo_path):
            return {"tag": None, "primary_stack": [], "repo_url": None, "live_url": None, "deployed": None}

        readme_text = self._read_readme(repo_path)
        manifest_stack = self._scan_manifests(repo_path)
        readme_stack = self._extract_stack_from_readme(readme_text)

        # Merge unique stack items with canonical casing
        seen = set()
        combined_stack = []
        for item in manifest_stack + readme_stack:
            item_norm = item.lower()
            if item_norm not in seen:
                seen.add(item_norm)
                combined_stack.append(item)

        # Extract track / tag from README
        detected_tag = self._extract_tag_from_readme(readme_text, fallback_name)
        
        # Discover in-repo link (git remote or README) and live deployment link
        repo_url = self._extract_repo_url(readme_text, repo_path)
        live_url = self._extract_live_url(readme_text)
        deployed = True if live_url else False

        return {
            "tag": detected_tag,
            "primary_stack": combined_stack,
            "repo_url": repo_url,
            "live_url": live_url,
            "deployed": deployed
        }

    def _read_readme(self, repo_path: str) -> str:
        for fname in ["README.md", "readme.md", "README", "readme.markdown"]:
            p = os.path.join(repo_path, fname)
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        return f.read()
                except Exception:
                    pass
        return ""

    def _scan_manifests(self, repo_path: str) -> List[str]:
        stack = []
        # Check package.json (root or frontend/)
        for p in [os.path.join(repo_path, "package.json"), os.path.join(repo_path, "frontend", "package.json")]:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        data = json.load(f)
                        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                        for dep in deps.keys():
                            dep_lower = dep.lower()
                            if "next" in dep_lower and "next-auth" not in dep_lower: stack.append("Next.js")
                            elif "react" in dep_lower: stack.append("React")
                            elif "typescript" in dep_lower: stack.append("TypeScript")
                            elif "tailwindcss" in dep_lower: stack.append("TailwindCSS")
                            elif "vite" in dep_lower: stack.append("Vite")
                except Exception:
                    pass

        # Check requirements.txt or pyproject.toml
        for p in [os.path.join(repo_path, "requirements.txt"), os.path.join(repo_path, "backend", "requirements.txt"), os.path.join(repo_path, "pyproject.toml")]:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().lower()
                        if "fastapi" in text: stack.append("FastAPI")
                        if "langgraph" in text: stack.append("LangGraph")
                        if "qdrant" in text: stack.append("Qdrant")
                        if "chromadb" in text: stack.append("ChromaDB")
                        if "asyncpg" in text or "psycopg" in text: stack.append("PostgreSQL")
                        if "google-genai" in text or "google-adk" in text: stack.append("Google ADK")
                        if "firestore" in text or "google-cloud-firestore" in text: stack.append("Firestore")
                        if "redis" in text: stack.append("Redis")
                        if "celery" in text: stack.append("Celery")
                        if "unsloth" in text: stack.append("Unsloth")
                except Exception:
                    pass
        
        # If any python files exist, ensure Python is in stack
        if any(f.endswith(".py") for root, _, files in os.walk(repo_path) for f in files[:20]):
            stack.insert(0, "Python")

        return stack

    def _clean_readme_text(self, text: str) -> str:
        """Strips fenced code blocks to prevent sample configs from polluting detection."""
        return re.sub(r'```[\s\S]*?```', '', text)

    def _extract_stack_from_readme(self, text: str) -> List[str]:
        cleaned = self._clean_readme_text(text)
        if not cleaned:
            return []
        found = []
        text_lower = cleaned.lower()
        for kw, canonical in TECH_KEYWORDS:
            # Word boundary search
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                if canonical not in found:
                    found.append(canonical)
        return found

    def _extract_tag_from_readme(self, text: str, fallback_name: str) -> Optional[str]:
        cleaned = self._clean_readme_text(text)
        if not cleaned:
            return None
        
        # Check for GitResume / Portfolio Agent tagline
        if "resume" in fallback_name.lower() or "git-resume" in cleaned.lower() or "gitresume" in cleaned.lower():
            return "Autonomous Multi-Agent Resume & Portfolio Intelligence Engine"

        # Check for Hackathon / Track patterns
        track_match = re.search(r'(?:hackathon submission for the|track:?)\s*[*_`]*([A-Za-z0-9\s]+?)[*_`]*\s*track', cleaned, re.IGNORECASE)
        if track_match:
            track_name = track_match.group(1).strip()
            return f"All Things Agentic Hackathon ({track_name.title()} Track)"

        # Check for OpenAI Build Week
        if "openai build week" in cleaned.lower() or "build week" in cleaned.lower():
            return "OpenAI Build Week Submission"

        # Check for Clinical / Research
        if "clinical" in cleaned.lower() or "research" in cleaned.lower():
            return "Clinical Research Intelligence"

        return None

    def _extract_repo_url(self, text: str, repo_path: str) -> Optional[str]:
        # 1. Try git remote first
        remote_url = get_git_remote_url(repo_path)
        if remote_url:
            return remote_url

        if not text:
            return None

        # 2. Try markdown repo badge / link
        match = re.search(r'\[(?:Code Repository|Repository|GitHub|Repo|Code)\]\((https?://github\.com/[^\)\s]+)\)', text, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            return url[:-4] if url.endswith(".git") else url

        # 3. Try any explicit github repo url matching pattern
        match_gh = re.search(r'(https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', text)
        if match_gh:
            url = match_gh.group(1).strip()
            if not url.endswith("/issues") and not url.endswith("/pulls"):
                return url

        return None

    def _extract_live_url(self, text: str) -> Optional[str]:
        if not text:
            return None
        # Try markdown live links: [Live App](url) or [Hosted App](url)
        match = re.search(r'\[(?:Live App|Live Demo|Hosted App|Live Product|Demo|Live)\]\((https?://[^\)\s]+)\)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Try labeled text: **Hosted app:** https://... or Live App: https://...
        match_text = re.search(r'(?:Hosted app|Live app|Live URL|Live Demo):\s*(https?://[^\s\)\`]+)', text, re.IGNORECASE)
        if match_text:
            return match_text.group(1).strip()

        return None

    def auto_sync_yaml(self, config_path: str = "gitresume.yaml") -> Tuple[bool, List[str]]:
        """Automatically updates gitresume.yaml if README or manifests have newer tags/stacks/links."""
        try:
            resolved_path = find_config_path(config_path)
        except Exception:
            return False, []

        with open(resolved_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        changes = []
        repositories = data.get("repositories", [])
        
        for repo in repositories:
            name = repo.get("name", "")
            path = repo.get("path", "")
            current_tag = repo.get("tag")
            current_stack = repo.get("primary_stack", [])
            current_repo_url = repo.get("repo_url")
            current_live_url = repo.get("live_url")
            current_deployed = repo.get("deployed")

            discovered = self.discover_repo_metadata(path, name)
            
            # Check tag update
            if discovered.get("tag") and discovered["tag"] != current_tag:
                old_tag = current_tag
                repo["tag"] = discovered["tag"]
                changes.append(f"[{name}] Updated tag: '{old_tag}' -> '{discovered['tag']}'")

            # Check primary_stack update
            discovered_stack = discovered.get("primary_stack", [])
            if discovered_stack:
                merged_stack = list(current_stack)
                added = []
                for s in discovered_stack:
                    if s not in merged_stack:
                        merged_stack.append(s)
                        added.append(s)
                if added:
                    repo["primary_stack"] = merged_stack
                    changes.append(f"[{name}] Discovered new stack tools: +{', +'.join(added)}")

            # Check repo_url update
            if discovered.get("repo_url") and discovered["repo_url"] != current_repo_url and not current_repo_url:
                repo["repo_url"] = discovered["repo_url"]
                changes.append(f"[{name}] Discovered repo URL: {discovered['repo_url']}")

            # Check live_url update
            if discovered.get("live_url") and discovered["live_url"] != current_live_url and not current_live_url:
                repo["live_url"] = discovered["live_url"]
                repo["deployed"] = True
                changes.append(f"[{name}] Discovered live URL: {discovered['live_url']}")
            elif current_deployed is None and discovered.get("deployed") is not None:
                repo["deployed"] = discovered["deployed"]
                changes.append(f"[{name}] Set deployment status: {'Deployed' if discovered['deployed'] else 'In-Repo'}")

        if changes:
            with open(resolved_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
            return True, changes

        return False, []
