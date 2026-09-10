import os
import re
from typing import Dict, Any, Optional
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE

def add_hyperlink(paragraph, url: str, text: str, color: str = "0066CC", underline: bool = True, italic: bool = True, bold: bool = False):
    """Appends an active, clickable hyperlink to a paragraph with styling."""
    if not url:
        return None
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)

    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)

    if italic:
        i = OxmlElement('w:i')
        rPr.append(i)

    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)

    new_run.append(rPr)

    text_elem = OxmlElement('w:t')
    text_elem.text = text
    new_run.append(text_elem)

    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink

class DocxCompiler:
    """Modifies Word .docx resume templates with synthesized metrics and clickable hyperlinks."""

    def format_paragraph_with_links(self, paragraph, base_text: str, stats: Dict[str, Any], is_italic: bool = True):
        """Populates paragraph with base text and appends active clickable hyperlinks."""
        paragraph.text = base_text
        if paragraph.runs:
            paragraph.runs[0].italic = is_italic

        is_deployed = stats.get("deployed", False)
        live_url = stats.get("live_url")
        repo_url = stats.get("repo_url")

        if (is_deployed and live_url) or repo_url:
            sep_run = paragraph.add_run("  |  ")
            sep_run.italic = is_italic

            added = 0
            if is_deployed and live_url:
                lbl = paragraph.add_run("Live: ")
                lbl.italic = is_italic
                display_live = live_url.replace("https://", "").replace("http://", "").rstrip("/")
                if len(display_live) > 35:
                    display_live = display_live[:32] + "..."
                add_hyperlink(paragraph, live_url, display_live, color="0066CC", underline=True, italic=is_italic)
                added += 1

            if repo_url:
                if added > 0:
                    mid = paragraph.add_run(" | ")
                    mid.italic = is_italic
                lbl = paragraph.add_run("Repo: ")
                lbl.italic = is_italic
                display_repo = repo_url.replace("https://", "").replace("http://", "").rstrip("/")
                add_hyperlink(paragraph, repo_url, display_repo, color="0066CC", underline=True, italic=is_italic)

    # ------------------------------------------------------------------
    # Header / contact-line sync
    # ------------------------------------------------------------------
    def sync_header_location(self, doc, location: Optional[str]):
        """Keeps the header contact line's city in sync with developer.location in gitresume.yaml.

        Previously this field was baked into each .docx template and never touched by
        `sync`, so editing gitresume.yaml silently stopped propagating to the compiled
        resumes. This only rewrites the leading 'City, Country' segment of the run
        before the first '|' separator, so the phone/email/LinkedIn/GitHub hyperlinks
        that follow are left completely untouched.
        """
        if not location:
            return
        location = location.strip()
        # The contact line is always within the first few header paragraphs, and is the
        # only one whose leading run contains both a '|' separator and a long digit run
        # (the phone number) - that combination is what identifies it, not its index.
        candidates = doc.paragraphs[:6] if len(doc.paragraphs) >= 6 else doc.paragraphs
        for p in candidates:
            if not p.runs:
                continue
            first = p.runs[0]
            if "|" in first.text and re.search(r"\d{7,}", first.text):
                prefix, sep, rest = first.text.partition("|")
                if prefix.strip() != location:
                    first.text = f"{location}  |{rest}"
                break

    # ------------------------------------------------------------------
    # GitResume project entry
    # ------------------------------------------------------------------
    def _find_para_index(self, doc, prefix: str) -> Optional[int]:
        for i, p in enumerate(doc.paragraphs):
            if p.text.strip().startswith(prefix):
                return i
        return None

    def _find_stat_para(self, doc, header_prefix: str, fallback_idx: Optional[int] = None):
        """Returns the paragraph immediately after the project header that starts with
        header_prefix - every template puts that project's stat/link line right there.

        This replaces a hardcoded paragraph index for the same reason sync_header_location
        does: templates get edited (bullets added/removed) and a fixed index silently starts
        writing into the wrong paragraph the next time `sync` runs. fallback_idx is only used
        if the header text can't be found at all, as a safety net for an unexpected layout.
        """
        idx = self._find_para_index(doc, header_prefix)
        if idx is not None and idx + 1 < len(doc.paragraphs):
            return doc.paragraphs[idx + 1]
        if fallback_idx is not None and fallback_idx < len(doc.paragraphs):
            return doc.paragraphs[fallback_idx]
        return None

    def gitresume_clause(self, g_stats: Dict[str, Any], compact: bool = True) -> str:
        g_loc = g_stats.get("loc_k", "2.5K")
        g_commits = g_stats.get("commits", 17)
        if compact:
            return (
                f" GitResume: self-built multi-agent LLM pipeline (PyPI: git-resume-agent, "
                f"~{g_loc} LOC, {g_commits} commits) that synthesizes and adversarially verifies "
                f"grounded resume bullets from git history."
            )
        return (
            f"GitResume Agent: self-built multi-agent LLM pipeline (PyPI: git-resume-agent, "
            f"~{g_loc} LOC, {g_commits} commits) that synthesizes and adversarially verifies "
            f"grounded resume bullets from git history."
        )

    def append_gitresume_to_paragraph(self, doc, prefix: str, g_stats: Dict[str, Any], compact: bool = True) -> bool:
        """Idempotently appends (or refreshes) a GitResume mention onto an existing catch-all
        paragraph (e.g. the merged 'Other Projects' or 'SQuAD' line), identified by its
        leading text rather than a hardcoded index so it survives future template edits."""
        idx = self._find_para_index(doc, prefix)
        if idx is None:
            return False
        p = doc.paragraphs[idx]
        current = p.text
        marker = "GitResume"
        if marker in current:
            current = current.split(marker, 1)[0].rstrip()
        else:
            current = current.rstrip()
        clause = self.gitresume_clause(g_stats, compact=compact).strip()
        p.text = f"{current} {clause}" if current else clause
        return True

    def sync_gitresume_block(self, doc, g_stats: Dict[str, Any]):
        """Idempotently inserts (or refreshes) a standalone GitResume project entry
        (header + stack line + bullet) immediately before EDUCATION, for templates that
        keep discrete project sections rather than one merged 'Other Projects' paragraph.
        """
        edu_idx = self._find_para_index(doc, "EDUCATION")
        if edu_idx is None:
            return False

        gr_idx = self._find_para_index(doc, "GitResume")

        g_loc = g_stats.get("loc_k", "2.5K")
        g_files = g_stats.get("files", 22)
        g_commits = g_stats.get("commits", 17)
        header_text = "GitResume — Autonomous Resume & Portfolio Intelligence Agent\t"
        stack_text = f"Python, Typer, Rich, Ollama, python-docx  |  ~{g_loc} LOC across {g_files} files, {g_commits} commits"
        bullet_text = (
            "Self-built a multi-agent pipeline (Inspector → SchemaDiscoverer → Synthesizer → "
            "GroundingVerifier) that scans git history/AST, synthesizes quantified resume bullets via "
            "LLM, and adversarially verifies every metric against commit diffs before compiling to "
            "Word/PDF with native hyperlinks — published to PyPI as git-resume-agent; runs on every "
            "commit via a git hook."
        )

        if gr_idx is not None:
            # Already present from a prior sync - just refresh the stats line in place.
            if gr_idx + 1 < len(doc.paragraphs):
                self.format_paragraph_with_links(doc.paragraphs[gr_idx + 1], stack_text, g_stats, is_italic=True)
            return True

        # Clone formatting from the CareFlow entry (always present) so the new block
        # matches the template's fonts/spacing instead of falling back to plain defaults.
        cf_idx = self._find_para_index(doc, "CareFlow Intelligence")
        header_style = doc.paragraphs[cf_idx].style if cf_idx is not None else None
        stack_style = doc.paragraphs[cf_idx + 1].style if cf_idx is not None and cf_idx + 1 < len(doc.paragraphs) else None
        bullet_style = doc.paragraphs[cf_idx + 2].style if cf_idx is not None and cf_idx + 2 < len(doc.paragraphs) else None
        cf_header_run = doc.paragraphs[cf_idx].runs[0] if cf_idx is not None and doc.paragraphs[cf_idx].runs else None

        edu_para = doc.paragraphs[edu_idx]

        header_p = edu_para.insert_paragraph_before("", style=header_style)
        r = header_p.add_run(header_text)
        if cf_header_run is not None:
            r.bold = cf_header_run.bold
            r.font.size = cf_header_run.font.size
            r.font.name = cf_header_run.font.name
        else:
            r.bold = True

        stack_p = edu_para.insert_paragraph_before("", style=stack_style)
        self.format_paragraph_with_links(stack_p, stack_text, g_stats, is_italic=True)

        edu_para.insert_paragraph_before(bullet_text, style=bullet_style)
        return True

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------
    def update_resume(self, file_path: str, persona_id: str, repo_stats: Dict[str, Dict[str, Any]], developer_location: Optional[str] = None) -> bool:
        if not os.path.exists(file_path):
            return False

        doc = docx.Document(file_path)

        # Keep the header city in sync with gitresume.yaml on every persona, every sync.
        self.sync_header_location(doc, developer_location)

        f_stats = repo_stats.get("FundersAI", {})
        t_stats = repo_stats.get("TalentOS", {})
        c_stats = repo_stats.get("CareFlow", {})
        g_stats = repo_stats.get("GitResume", {})

        f_loc = f_stats.get("loc_k", "145K")
        f_files = f_stats.get("files", 760)
        f_commits = f_stats.get("commits", 402)
        f_tests = f"{f_stats.get('test_suites', 120)}+"

        t_loc = t_stats.get("loc_k", "32K")
        t_files = t_stats.get("files", 134)
        t_commits = t_stats.get("commits", 51)

        if persona_id in ("master", "master_2page"):
            # P19: FundersAI subheader
            if len(doc.paragraphs) > 19:
                f_base = f"Solo-built, Apr–Aug 2026 — ~{f_loc} lines of code across {f_files} files, {f_commits} commits, {f_tests} test suites — submitted to OpenAI Build Week"
                self.format_paragraph_with_links(doc.paragraphs[19], f_base, f_stats, is_italic=True)

            # P38 & P39: TalentOS
            if len(doc.paragraphs) > 39:
                doc.paragraphs[38].runs[0].text = "TalentOS — Autonomous Opportunity Intelligence Platform (All Things Agentic Hackathon)"
                t_base = f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  Solo-built, Aug 2026 — ~{t_loc} LOC across {t_files} files, {t_commits} commits, 235+ test suite"
                self.format_paragraph_with_links(doc.paragraphs[39], t_base, t_stats, is_italic=True)

            # Standalone GitResume section before EDUCATION (comprehensive doc has room for it).
            self.sync_gitresume_block(doc, g_stats)

        elif persona_id == "master_1page":
            # FundersAI subheader - found relative to the "FundersAI —" project header
            # rather than a fixed index, so inserting/removing bullets on this template
            # (e.g. to fill out the page) can't silently misalign future syncs.
            f_stat_para = self._find_stat_para(doc, "FundersAI —", fallback_idx=16)
            if f_stat_para is not None:
                f_base = f"Python, FastAPI, Next.js, Supabase/pgvector, LangGraph, Groq, OpenAI, Cloudflare R2, Kubernetes (K3s)\nSolo-built, Apr–Aug 2026 — ~{f_loc} LOC across {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                self.format_paragraph_with_links(f_stat_para, f_base, f_stats, is_italic=True)

            # TalentOS - same header-relative lookup.
            t_stat_para = self._find_stat_para(doc, "TalentOS —", fallback_idx=21)
            if t_stat_para is not None:
                t_base = f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  ~{t_loc} LOC across {t_files} files, {t_commits} commits, 235+ test suite"
                self.format_paragraph_with_links(t_stat_para, t_base, t_stats, is_italic=True)

            # Space is tight on a strict 1-pager - fold GitResume into the existing
            # 'Other Projects & Research' line instead of adding new paragraphs.
            self.append_gitresume_to_paragraph(doc, "SQuAD QA Benchmarking", g_stats, compact=False)

        elif persona_id == "fde":
            if len(doc.paragraphs) > 16:
                f_base = f"Python, FastAPI, Next.js, LangGraph, Groq, OpenAI  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                self.format_paragraph_with_links(doc.paragraphs[16], f_base, f_stats, is_italic=True)
            if len(doc.paragraphs) > 20:
                doc.paragraphs[19].text = "TalentOS — Autonomous Opportunity Intelligence Platform (All Things Agentic Hackathon)\t"
                doc.paragraphs[19].runs[0].bold = True
                t_base = f"Python, Google ADK, LangGraph, Next.js, Firestore, Google Cloud Run  |  ~{t_loc} LOC across {t_files} files, {t_commits} commits, 235+ test suite"
                self.format_paragraph_with_links(doc.paragraphs[20], t_base, t_stats, is_italic=True)

            # fde has no catch-all paragraph - give GitResume its own compact block.
            self.sync_gitresume_block(doc, g_stats)

        elif persona_id == "genai":
            if len(doc.paragraphs) > 15:
                f_base = f"Python, FastAPI, Next.js, Supabase/pgvector, LangGraph, Groq, OpenAI  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                self.format_paragraph_with_links(doc.paragraphs[15], f_base, f_stats, is_italic=True)
            if len(doc.paragraphs) > 24:
                t_links_str = " | " + t_stats.get("formatted_links", "") if t_stats.get("formatted_links") else ""
                doc.paragraphs[24].text = (
                    f"TalentOS (All Things Agentic Hackathon, Taskmaster Track): dual-pipeline multi-agent platform (Google ADK, LangGraph, Gemini on Vertex AI) generating tailored resumes/pitches with 91% deterministic pre-filtering before LLM calls — ~{t_loc} LOC, {t_files} files, 235+ test suite{t_links_str}. FundersAI Reports: decoupled LangGraph microservice on a K3s/EC2 Kubernetes deployment. SQuAD QA Benchmarking: fine-tuned BERT/BiDAF/DistilBERT; published research paper."
                    + self.gitresume_clause(g_stats, compact=True)
                )

        elif persona_id == "ai_engineer":
            if len(doc.paragraphs) > 16:
                f_base = f"Python, FastAPI, Next.js, Supabase/pgvector, LangGraph, Groq, OpenAI, Cloudflare R2  |  ~{f_loc} LOC, {f_files} files, {f_commits} commits, {f_tests} test suites — OpenAI Build Week"
                self.format_paragraph_with_links(doc.paragraphs[16], f_base, f_stats, is_italic=True)
            if len(doc.paragraphs) > 25:
                t_links_str = " | " + t_stats.get("formatted_links", "") if t_stats.get("formatted_links") else ""
                doc.paragraphs[25].text = (
                    f"TalentOS (All Things Agentic Hackathon, Taskmaster Track): dual-pipeline autonomous agent platform (Google ADK, LangGraph, Firestore) ingesting ~2,500 postings/run across 8 sources with 91% pre-filtering and a 3-state evaluator+drafter chain — ~{t_loc} LOC, {t_files} files, 235+ tests{t_links_str}. FundersAI Reports: decoupled LangGraph microservice on a 2-replica Kubernetes Deployment (K3s/AWS EC2). SQuAD QA Benchmarking: fine-tuned/benchmarked BERT/BiDAF/DistilBERT; published as a research paper."
                    + self.gitresume_clause(g_stats, compact=True)
                )

        doc.save(file_path)
        return True
