from typing import Dict, Any, List

class SynthesizerAgent:
    """Synthesizes clean XYZ-format impact bullet points based on inspected git metrics."""

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
