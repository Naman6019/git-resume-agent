import os
from typing import Dict, Any
import docx

class DocxCompiler:
    """Modifies Word .docx resume templates with synthesized metrics while preserving styles."""

    def update_resume(self, file_path: str, persona_id: str, repo_stats: Dict[str, Dict[str, Any]]) -> bool:
        if not os.path.exists(file_path):
            return False

        doc = docx.Document(file_path)
        f_stats = repo_stats.get("FundersAI", {})
        t_stats = repo_stats.get("TalentOS", {})

        f_loc = f_stats.get("loc_k", "145K")
        f_files = f_stats.get("files", 760)
        f_commits = f_stats.get("commits", 402)
        f_tests = f"{f_stats.get('test_suites', 120)}+"

        t_loc = t_stats.get("loc_k", "32K")
        t_files = t_stats.get("files", 134)
        t_commits = t_stats.get("commits", 51)

        if persona_id == "master":
            # P19: FundersAI subheader
            if len(doc.paragraphs) > 19:
                doc.paragraphs[19].text = f"Solo-built, Apr–Aug 2026 — ~{f_loc} lines of code across {f_files} files, {f_commits} commits, {f_tests} test suites — submitted to OpenAI Build Week"
                if doc.paragraphs[19].runs:
                    doc.paragraphs[19].runs[0].italic = True

            # P38 & P39: TalentOS
            if len(doc.paragraphs) > 39:
                doc.paragraphs[38].runs[0].text = "TalentOS — Autonomous Opportunity Intelligence Platform (All Things Agentic Hackathon)"
                doc.paragraphs[39].text = f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  Solo-built, Aug 2026 — ~{t_loc} LOC across {t_files} files, {t_commits} commits, 235+ test suite"
                if doc.paragraphs[39].runs:
                    doc.paragraphs[39].runs[0].italic = True

        elif persona_id == "fde":
            if len(doc.paragraphs) > 16:
                doc.paragraphs[16].text = f"Python, FastAPI, Next.js, LangGraph, Groq, OpenAI  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                if doc.paragraphs[16].runs:
                    doc.paragraphs[16].runs[0].italic = True
            if len(doc.paragraphs) > 20:
                doc.paragraphs[19].text = "TalentOS — Autonomous Opportunity Intelligence Platform (All Things Agentic Hackathon)	"
                doc.paragraphs[19].runs[0].bold = True
                doc.paragraphs[20].text = f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  ~{t_loc} LOC across {t_files} files, {t_commits} commits, 235+ test suite"
                if doc.paragraphs[20].runs:
                    doc.paragraphs[20].runs[0].italic = True

        elif persona_id == "genai":
            if len(doc.paragraphs) > 15:
                doc.paragraphs[15].text = f"Python, FastAPI, Next.js, Supabase/pgvector, LangGraph, Groq, OpenAI  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                if doc.paragraphs[15].runs:
                    doc.paragraphs[15].runs[0].italic = True
            if len(doc.paragraphs) > 24:
                doc.paragraphs[24].text = f"TalentOS (All Things Agentic Hackathon, Taskmaster Track): dual-pipeline multi-agent platform (Google ADK, LangGraph, Gemini on Vertex AI) generating tailored resumes/pitches with 91% deterministic pre-filtering before LLM calls — ~{t_loc} LOC, {t_files} files, 235+ test suite. FundersAI Reports: decoupled LangGraph microservice on a K3s/EC2 Kubernetes deployment. SQuAD QA Benchmarking: fine-tuned BERT/BiDAF/DistilBERT; published research paper."

        elif persona_id == "ai_engineer":
            if len(doc.paragraphs) > 16:
                doc.paragraphs[16].text = f"Python, FastAPI, Next.js, Supabase/pgvector, LangGraph, Groq, OpenAI, Cloudflare R2  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                if doc.paragraphs[16].runs:
                    doc.paragraphs[16].runs[0].italic = True
            if len(doc.paragraphs) > 25:
                doc.paragraphs[25].text = f"TalentOS (All Things Agentic Hackathon, Taskmaster Track): dual-pipeline autonomous agent platform (Google ADK, LangGraph, Firestore) ingesting ~2,500 postings/run across 8 sources with 91% pre-filtering and a 3-state evaluator+drafter chain — ~{t_loc} LOC, {t_files} files, 235+ tests. FundersAI Reports: decoupled LangGraph microservice on a 2-replica Kubernetes Deployment (K3s/AWS EC2). SQuAD QA Benchmarking: fine-tuned/benchmarked BERT/BiDAF/DistilBERT; published as a research paper."

        doc.save(file_path)
        return True
