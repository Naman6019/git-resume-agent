from typing import Dict, Any, List
from git_resume.utils.llm_client import LLMClient
from git_resume.agents.verifier import GroundingVerifierAgent

class SynthesizerAgent:
    """Synthesizes high-impact Google XYZ-format bullet points based on inspected git metrics and LLM reasoning."""

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()
        self.verifier = GroundingVerifierAgent()

    def generate_ai_bullet(self, repo_data: Dict[str, Any], persona_emphasis: List[str]) -> Dict[str, Any]:
        """Uses LLM reasoning to draft a fresh, grounded bullet point from git commits and diffs."""
        name = repo_data.get("name", "Project")
        tag = repo_data.get("tag", "")
        stack = ", ".join(repo_data.get("stack", []))
        commits = repo_data.get("recent_commits", [])
        commit_msgs = [c.get("message", "") for c in commits[:6]]
        emphasis = ", ".join(persona_emphasis)

        prompt = f"""You are an elite Applied AI and Systems Engineer resume writer.
Project: {name} ({tag})
Tech Stack: {stack}
Recent Git Commits:
{chr(10).join(f"- {m}" for m in commit_msgs)}

Target Emphasis: {emphasis}

Task: Synthesize exactly 1 high-impact resume bullet point following the Google XYZ format:
"Accomplished [X: clear technical achievement], as measured by [Y: quantifiable metric or architectural guarantee], by doing [Z: specific technical implementation/tools]."

Rules:
1. Ground every claim strictly in the tech stack and commits above. Do NOT hallucinate unmentioned technologies.
2. Start directly with a strong past-tense action verb (e.g., Engineered, Architected, Designed, Shipped).
3. Do not include introductory text or quotes. Output ONLY the single bullet point.
"""
        system_prompt = "You write precise, highly quantified, senior-level engineering bullet points without fluff."
        raw_bullet = self.llm.generate(prompt, system_prompt=system_prompt)
        
        # Verify grounding
        is_valid, reason = self.verifier.verify_bullet(raw_bullet, repo_data)

        return {
            "bullet": raw_bullet,
            "verified": is_valid,
            "verification_note": reason
        }

    def synthesize_fundersai(self, stats: Dict[str, Any]) -> str:
        loc_k = stats.get("loc_k", "145K")
        files = stats.get("files", 760)
        commits = stats.get("commits", 402)
        tests = f"{stats.get('test_suites', 120)}+"
        return f"Solo-built, Apr–Aug 2026 — ~{loc_k} lines of code across {files} files, {commits} commits, {tests} test suites — submitted to OpenAI Build Week"

    def synthesize_talentos(self, stats: Dict[str, Any]) -> str:
        loc_k = stats.get("loc_k", "32K")
        files = stats.get("files", 134)
        commits = stats.get("commits", 51)
        return f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  Solo-built, Aug 2026 — ~{loc_k} LOC across {files} files, {commits} commits, 235+ test suite"
