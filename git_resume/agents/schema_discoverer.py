import os
import re
import json
import yaml
from typing import Dict, Any, List, Tuple, Optional

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
            return {"tag": None, "primary_stack": []}

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

        return {
            "tag": detected_tag,
            "primary_stack": combined_stack
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

    def _extract_stack_from_readme(self, text: str) -> List[str]:
        if not text:
            return []
        found = []
        text_lower = text.lower()
        for kw, canonical in TECH_KEYWORDS:
            # Word boundary search
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                if canonical not in found:
                    found.append(canonical)
        return found

    def _extract_tag_from_readme(self, text: str, fallback_name: str) -> Optional[str]:
        if not text:
            return None
        
        # Check for Hackathon / Track patterns
        track_match = re.search(r'(?:hackathon submission for the|track:?)\s*[*_`]*([A-Za-z0-9\s]+?)[*_`]*\s*track', text, re.IGNORECASE)
        if track_match:
            track_name = track_match.group(1).strip()
            return f"All Things Agentic Hackathon ({track_name.title()} Track)"

        # Check for OpenAI Build Week
        if "openai build week" in text.lower() or "build week" in text.lower():
            return "OpenAI Build Week Submission"

        # Check for Clinical / Research
        if "clinical" in text.lower() or "research" in text.lower():
            return "Clinical Research Intelligence"

        return None

    def auto_sync_yaml(self, config_path: str = "gitresume.yaml") -> Tuple[bool, List[str]]:
        """Automatically updates gitresume.yaml if README or manifests have newer tags/stacks."""
        if not os.path.exists(config_path):
            return False, []

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        changes = []
        repositories = data.get("repositories", [])
        
        for repo in repositories:
            name = repo.get("name", "")
            path = repo.get("path", "")
            current_tag = repo.get("tag")
            current_stack = repo.get("primary_stack", [])

            discovered = self.discover_repo_metadata(path, name)
            
            # Check tag update
            if discovered.get("tag") and discovered["tag"] != current_tag:
                old_tag = current_tag
                repo["tag"] = discovered["tag"]
                changes.append(f"[{name}] Updated tag: '{old_tag}' -> '{discovered['tag']}'")

            # Check primary_stack update
            discovered_stack = discovered.get("primary_stack", [])
            if discovered_stack:
                # Merge existing stack items with any newly discovered ones
                merged_stack = list(current_stack)
                added = []
                for s in discovered_stack:
                    if s not in merged_stack:
                        merged_stack.append(s)
                        added.append(s)
                if added:
                    repo["primary_stack"] = merged_stack
                    changes.append(f"[{name}] Discovered new stack tools: +{', +'.join(added)}")

        if changes:
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
            return True, changes

        return False, []
