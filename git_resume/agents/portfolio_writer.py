"""
PortfolioDescriptionAgent: watches a tracked repo's README for meaningful
changes and, when one lands, proposes updated wording for that project's
entry in the portfolio site's `portfolioProjects` array -- as a reviewable
PR, never a direct push. Silence is the default: no LLM, no meaningful
README change, or a proposal that fails grounding all result in skipping,
not in guessing.
"""
import re
from typing import Any, Dict, List, Optional

from git_resume.config import RepoConfig
from git_resume.utils.llm_client import LLMClient
from git_resume.utils.git_utils import get_file_diff
from git_resume.compilers.portfolio_ts_editor import extract_current_fields

# The exact string LLMClient._heuristic_synthesis() returns when every real
# provider failed. If we see this, there was no real model behind the answer
# -- treat it as a failure, never as a proposal.
_HEURISTIC_SENTINEL = "Architected and deployed modular system components with end-to-end testing, error recovery, and production telemetry."

_FIELD_LINE = re.compile(r"^(SUMMARY|PROBLEM|BUILD|OUTCOME|LIMITATIONS|STACK):\s*(.+)$", re.MULTILINE)


class PortfolioDescriptionAgent:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()

    def propose(
        self,
        repo: RepoConfig,
        readme_text: str,
        readme_diff: str,
        portfolio_source: str,
    ) -> Optional[Dict[str, Any]]:
        """Returns a dict of {field: new_value} for fields worth changing, or
        None if nothing should change (including on any failure)."""
        try:
            current = extract_current_fields(portfolio_source, repo.portfolio_slug)
        except Exception:
            return None
        if not current:
            return None

        readme_excerpt = readme_text[:6000]
        diff_excerpt = readme_diff[:4000]

        prompt = f"""You are editing one project entry on a developer's live portfolio website.
The site's voice is dry, technical, and evidence-first: every sentence must be
something the README actually supports. Never invent metrics, numbers, or
capabilities that are not present in the README below.

CURRENT SITE COPY for this project:
SUMMARY: {current.get("summary", "")}
PROBLEM: {current.get("problem", "")}
BUILD: {current.get("build", "")}
OUTCOME: {current.get("outcome", "")}
LIMITATIONS: {current.get("limitations", "")}
STACK: {", ".join(current.get("stack", []))}

WHAT CHANGED IN THE REPO'S README (diff):
{diff_excerpt if diff_excerpt else "(no diff available)"}

FULL CURRENT README (for context/grounding):
{readme_excerpt}

TASK: Decide whether the diff above describes a change material enough that
the site copy is now stale or inaccurate (e.g. a new capability, a changed
boundary/limitation, a new or dropped piece of the stack, a status change
described in prose). Cosmetic README edits (typos, formatting, badge
shuffling, unchanged meaning) do NOT warrant a rewrite.

If nothing warrants a change, output exactly: NO_CHANGE

Otherwise output ONLY the fields that must change, one per line, in this exact
format (omit any field that stays the same -- do not restate unchanged
fields):
SUMMARY: <one sentence, present tense, matches existing tone>
PROBLEM: <one sentence>
BUILD: <one or two sentences>
OUTCOME: <one sentence>
LIMITATIONS: <one sentence naming a real, current boundary>
STACK: <comma-separated list, only if it changed>

Do not add commentary, headings, or markdown. Do not wrap the output in a code
block."""

        system_prompt = (
            "You are a precise technical editor. You only ever state what the "
            "provided source material supports. When in doubt, you prefer no "
            "change over an unsupported one."
        )

        response = self.llm.generate(prompt, system_prompt=system_prompt)

        if not response or response.strip() == _HEURISTIC_SENTINEL:
            return None  # no working LLM behind this -- never guess

        cleaned = response.strip()
        if cleaned.upper().startswith("NO_CHANGE"):
            return None

        matches = _FIELD_LINE.findall(cleaned)
        if not matches:
            return None

        proposed: Dict[str, Any] = {}
        for key, value in matches:
            value = value.strip()
            if not value:
                continue
            if key == "STACK":
                proposed["stack"] = [s.strip() for s in value.split(",") if s.strip()]
            else:
                proposed[key.lower()] = value

        return proposed or None

    def verify_grounded(self, proposed: Dict[str, Any], readme_text: str) -> List[str]:
        """Returns the list of proposed field keys that pass grounding, dropping
        any that cite something (a stack item, a number) absent from the
        README. Text fields with no checkable claim pass through as-is; this
        is a floor, not a substitute for the LLM's own instructions."""
        readme_lower = readme_text.lower()
        accepted: List[str] = []

        for key, value in proposed.items():
            if key == "stack":
                items = [s for s in value if s.lower() in readme_lower]
                if items:
                    proposed[key] = items
                    accepted.append(key)
                continue

            numbers = re.findall(r"\d[\d,.]*%?", str(value))
            if all(n in readme_text for n in numbers):
                accepted.append(key)
            # else: this field cites a number the README doesn't contain -- drop it

        return accepted
