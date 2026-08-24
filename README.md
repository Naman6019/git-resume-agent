# GitResume AI 🚀

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CLI](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-magenta.svg)](https://typer.tiangolo.com/)
[![Multi--Agent](https://img.shields.io/badge/Architecture-Multi--Agent%20Pipeline-orange.svg)](https://github.com/Naman6019/git-resume-agent)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20Cloud%20%7C%20Local-purple.svg)](https://ollama.com)
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20Passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Autonomous Multi-Agent Resume & Portfolio Intelligence Engine**  
> *Grounding your engineering resume directly in your active Git commit history, AST diffs, and codebase metrics — with zero hallucinations.*

---

## 💡 Why GitResume AI?

As developers and AI engineers, our codebases evolve every day — we ship features, refactor parsers, optimize vector retrieval latencies, and increase test coverage. Yet, our resumes remain static, outdated, and ungrounded.

**GitResume AI** automates the entire lifecycle of engineering credentials:
1. **Perceives** live git repositories (commits, lines of code, test suites, and AST diffs).
2. **Discovers** tech stack changes and hackathon tracks dynamically from repository `README.md` files and package manifests.
3. **Synthesizes** quantified achievement bullets following the **Google XYZ formula** (*"Accomplished X, measured by Y, by doing Z"*).
4. **Verifies** every claim against the codebase to prevent hallucinations.
5. **Compiles & Syncs** role-tailored Word (`.docx`) and headless PDF resumes directly to your public portfolio website.

---

## 🏗️ Multi-Agent Architecture

```
                                 ┌─────────────────────────────┐
                                 │     Active Git Repos        │
                                 │ (FundersAI, TalentOS, etc.) │
                                 └──────────────┬──────────────┘
                                                │
                                                ▼
 ┌───────────────────────────┐    ┌───────────────────────────┐
 │ 1. SCHEMA DISCOVERER AGENT│───▶│    gitresume.yaml Config  │
 │  * Scans READMEs & Badges │    │ (Tags, Stack, Personas)   │
 │  * Detects Manifest Deps  │    └─────────────┬─────────────┘
 └───────────────────────────┘                  │
                                                ▼
                                  ┌───────────────────────────┐
                                  │   2. INSPECTOR AGENT      │
                                  │  * Scans Commit History   │
                                  │  * Computes LOC & Tests   │
                                  │  * Extracts AST Diffs     │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │  3. SYNTHESIZER AGENT     │
                                  │  * Ollama Cloud / Local   │
                                  │  * Google XYZ Formula     │
                                  │  * Role-Specific Framing  │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │ 4. GROUNDING VERIFIER     │
                                  │  * Anti-Hallucination     │
                                  │  * Codebase Cross-Check   │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │  5. COMPILERS & SYNC      │
                                  │  * MS Word (.docx) Runs   │
                                  │  * Headless COM PDF       │
                                  │  * Portfolio Auto-Sync    │
                                  └───────────────────────────┘
```

### Agent Roles:
* **SchemaDiscoverer Agent**: Parses project `README.md` files, badges, and manifests (`package.json`, `pyproject.toml`, `requirements.txt`). When you add a tool or win a hackathon track, it updates `gitresume.yaml` in-place.
* **Inspector Agent**: Interrogates `git ls-files`, `git log`, and test directories across 100K+ lines of code in < 5ms without traversal bottlenecks.
* **Synthesizer Agent**: Employs flagship coding LLMs (e.g. `kimi-k2.7-code`, `deepseek-v4-pro`, `qwen2.5-coder`) via Ollama Cloud or local Ollama to craft high-impact accomplishment bullets.
* **Grounding Verifier Agent**: Acts as an adversarial critic, verifying that cited frameworks and performance metrics are mathematically grounded in the git history.
* **Persona Dispatcher & Compilers**: Modifies specific paragraph runs in Word `.docx` documents preserving exact typography, triggers MS Word COM automation for pixel-perfect PDF export, and syncs directly to public portfolio directories.

---

## ⚡ Quickstart & Installation

### 1. Clone & Install
```bash
git clone https://github.com/Naman6019/git-resume-agent.git
cd git-resume-agent

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows (or `source .venv/bin/activate` on Linux/macOS)

# Install editable package
pip install -e .
```

### 2. Configure Environment (Optional LLM Keys)
Copy `.env.example` to `.env`:
```env
# Option A: Ollama Cloud (No download needed, uses flagship models)
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_API_KEY=your_ollama_api_key

# Option B: Local Ollama (100% Free, Offline)
OLLAMA_BASE_URL=http://127.0.0.1:11434

# Option C: Google Gemini Free Endpoint
GEMINI_API_KEY=AIzaSy...
```

---

## 🕹️ CLI Usage

### 1. Auto-Discover Schema from READMEs
Inspects configured repositories and syncs newly added tech tools or hackathon tags into `gitresume.yaml`:
```bash
git-resume auto-config
```

### 2. Live Codebase Intelligence Dashboard
Displays real-time commit counts, file statistics, total lines of code, and test suites across all tracked repositories:
```bash
git-resume scan
```

### 3. Synthesize Grounded Achievement Bullets
Uses multi-agent reasoning over recent git commits to generate role-specific Google XYZ bullets:
```bash
# Generate bullet for Forward-Deployed Engineer role
git-resume generate --repo FundersAI --persona fde

# Generate bullet for Generative AI Engineer role
git-resume generate --repo TalentOS --persona genai

# Generate bullet for AI/ML Engineer role
git-resume generate --repo CareFlow --persona ai_engineer
```

### 4. Full End-to-End Multi-Agent Sync
Runs the entire pipeline (Inspect $\rightarrow$ Synthesize $\rightarrow$ Verify $\rightarrow$ Compile `.docx` $\rightarrow$ Export `.pdf` $\rightarrow$ Sync to Portfolio):
```bash
git-resume sync
```

---

## ⚙️ Configuration (`gitresume.yaml`)

```yaml
version: "1.0"

developer:
  name: "Naman Manocha"
  email: "namanmanocha6019@gmail.com"
  github: "https://github.com/Naman6019"
  linkedin: "https://linkedin.com/in/naman-d-manocha"
  location: "Mumbai, India"

repositories:
  - name: "FundersAI"
    path: "C:/Users/naman/OneDrive/Desktop/FundersAI"
    tag: "OpenAI Build Week Submission"
    primary_stack: ["Python", "FastAPI", "React", "TypeScript", "Vite", "TailwindCSS", "Qdrant", "PostgreSQL"]

  - name: "TalentOS"
    path: "C:/Users/naman/OneDrive/Desktop/ALLThingsAgentic"
    tag: "All Things Agentic Hackathon (Taskmaster Track)"
    primary_stack: ["Python", "Google ADK", "LangGraph", "Next.js", "Firestore", "Google Cloud Run"]

personas:
  - id: "fde"
    title: "Agentic AI / Forward-Deployed Engineer"
    resume_file: "Naman_Manocha_Agentic_AI_FDE_Resume.docx"
    emphasis: ["evals", "hybrid-search", "strict-abstention", "production-agents", "forward-deployed"]

  - id: "genai"
    title: "Generative AI Engineer"
    resume_file: "Naman_Manocha_GenAI_Engineer_Resume.docx"
    emphasis: ["rag", "vector-embeddings", "langgraph", "llm-pipelines", "tool-calling"]

output:
  formats: ["docx", "pdf"]
  resume_dir: "C:/Users/naman/OneDrive/Desktop/Personal/Resume"
  sync_paths:
    - "C:/Users/naman/OneDrive/Desktop/Personal/portfolio_site/public/resume"

llm:
  provider: "ollama"
  model: "kimi-k2.7-code"
  fallback_model: "gpt-4o-mini"
```

---

## 🪝 Zero-Touch Git Hook Integration

To automatically sync your resume every time you make a commit in your project repositories, install the post-commit hook:

```bash
python scripts/install_hooks.py
```

This creates `.git/hooks/post-commit` in each repository, triggering background inspection and compilation upon every `git commit`.

---

## 🧪 Testing

Run the automated unit test suite:
```bash
pytest tests/ -v
```
```
collected 5 items
tests/test_git_resume.py::test_load_config PASSED        [ 20%]
tests/test_git_resume.py::test_inspector_agent PASSED    [ 40%]
tests/test_git_resume.py::test_grounding_verifier PASSED [ 60%]
tests/test_git_resume.py::test_synthesizer_agent PASSED  [ 80%]
tests/test_git_resume.py::test_schema_discoverer PASSED  [100%]
====================== 5 passed in 0.62s ======================
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👤 Author

**Naman Manocha**  
* [GitHub (@Naman6019)](https://github.com/Naman6019)  
* [LinkedIn](https://linkedin.com/in/naman-d-manocha)  
* Email: namanmanocha6019@gmail.com
