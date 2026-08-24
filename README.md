# GitResume AI 🚀
> **Autonomous Multi-Agent Resume & Portfolio Intelligence Engine**

GitResume AI continuously inspects your local Git repositories, parses commit histories, code diffs, and test suites, and autonomously compiles grounded, role-tailored resumes (DOCX, PDF, Markdown, JSONResume).

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Scan your active repositories
python -m git_resume.cli scan

# 3. Compile all role-specific resumes and sync to portfolio
python -m git_resume.cli sync
```

---

## 🏗️ Architecture

1. **Inspector Agent:** Scans Git diffs, AST modifications, dependency additions, test suites, and LOC metrics.
2. **Synthesizer Agent:** Analyzes the semantic intent of code changes and generates structured XYZ-format bullets.
3. **Grounding Verifier Agent:** Anti-hallucination guardrail validating claims against commit hashes and dependency trees.
4. **Persona Dispatcher:** Routes achievements to target personas (FDE, GenAI, MLOps, Full-Stack).

---

## 📄 License
MIT © [Naman Manocha](https://github.com/Naman6019)
