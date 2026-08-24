# GitResume Agent 🚀

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CLI](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-magenta.svg)](https://typer.tiangolo.com/)
[![Multi--Agent](https://img.shields.io/badge/Architecture-Autonomous%20Agentic%20Pipeline-orange.svg)](https://github.com/Naman6019/git-resume-agent)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20Cloud%20%7C%20Local-purple.svg)](https://ollama.com)
[![Tests](https://img.shields.io/badge/Tests-5%2F5%20Passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Autonomous Git-Driven Resume & Portfolio Agent**  
> *A zero-touch agentic pipeline that perceives git diffs and codebase ASTs upon commit, synthesizes grounded Google XYZ accomplishment bullets with adversarial critique, and autonomously compiles role-tailored resumes directly to production portfolio endpoints.*

---

## 💡 Why GitResume Agent?

As software and AI engineers, our codebases evolve every day — we ship features, refactor parsers, optimize vector retrieval latencies, and increase test coverage. Yet, our resumes remain static, outdated, and ungrounded.

**GitResume Agent** automates the entire lifecycle of engineering credentials as an event-driven CI/CD system:
1. **Perception**: Interrogates active Git repositories (commits, lines of code, test suites, and AST diffs) in < 5ms.
2. **Schema Discovery**: Dynamically detects tech stack additions and hackathon track changes from `README.md` files and package manifests, updating configuration in-place.
3. **Reasoned Synthesis**: Synthesizes quantified achievement bullets following the **Google XYZ formula** (*"Accomplished X, measured by Y, by doing Z"*).
4. **Adversarial Critique**: Validates every cited metric and library against the commit AST to mathematically eliminate hallucinations.
5. **Multi-Format Execution & Sync**: Injects fresh bullets into Word (`.docx`) runs preserving exact styling, exports headless PDFs via COM automation, and syncs directly to your live portfolio website.

---

## 🤖 Truly Autonomous: How It Works

GitResume Agent operates on an **event-driven, zero-touch autonomy loop**:

```
                       ┌─────────────────────────────────────┐
                       │           DEVELOPER ACTION          │
                       │          `git commit -m "..."`      │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼ (Post-Commit Hook Trigger)
 ┌──────────────────────────────────────────────────────────────────────────────────┐
 │                          AUTONOMOUS AGENT PIPELINE                               │
 │                                                                                  │
 │  1. PERCEPTION           2. SCHEMA DISCOVERY      3. REASONING & SYNTHESIS       │
 │  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────────────────┐   │
 │  │ InspectorAgent   │───▶│ SchemaDiscoverer │───▶│ SynthesizerAgent          │   │
 │  │ Git Log / AST    │    │ README & Badges  │    │ Flagship Ollama Cloud LLM │   │
 │  └──────────────────┘    └──────────────────┘    └─────────────┬─────────────┘   │
 │                                                                │                 │
 │                                                                ▼                 │
 │  5. DUAL-TIER SYNC       4. COMPILATION           4. ADVERSARIAL CRITIQUE        │
 │  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────────────────┐   │
 │  │ Portfolio / Web  │◀───│ Docx & PDF Engine│◀───│ GroundingVerifierAgent    │   │
 │  │ Public Mirroring │    │ Headless Word COM│    │ AST / Metric Verification │   │
 │  └──────────────────┘    └──────────────────┘    └───────────────────────────┘   │
 └──────────────────────────────────────────────────────────────────────────────────┘
```

* **Zero-Touch Git Hooks**: Once installed, you never need to manually trigger compilation. Committing to any project repository automatically initiates background resume updates.
* **In-Place Schema Auto-Sync**: Adding a new framework to `package.json` or a hackathon badge to `README.md` automatically mutates `gitresume.yaml` idempotently.
* **Deterministic Guardrails**: Human governance controls initial role personas and target paths, while multi-agent execution handles perception, critique, and artifact compilation.

---

## 🏗️ Multi-Agent Architecture

### Agent Roles:
* **SchemaDiscoverer Agent**: Parses project `README.md` files, badges, and manifests (`package.json`, `pyproject.toml`, `requirements.txt`). When you add a tool or win a hackathon track, it updates `gitresume.yaml` in-place.
* **Inspector Agent**: Interrogates `git ls-files`, `git log`, and test directories across 100K+ lines of code in < 5ms without traversal bottlenecks.
* **Synthesizer Agent**: Employs flagship coding LLMs (e.g. `kimi-k2.7-code`, `deepseek-v4-pro`, `qwen2.5-coder`) via Ollama Cloud or local Ollama to craft high-impact accomplishment bullets.
* **Grounding Verifier Agent**: Acts as an adversarial critic, verifying that cited frameworks and performance metrics are mathematically grounded in the git history.
* **Persona Dispatcher & Compilers**: Modifies specific paragraph runs in Word `.docx` documents preserving exact typography, triggers MS Word COM automation for pixel-perfect PDF export, and syncs directly to public portfolio directories.

---

## 📂 Where Generated Resumes Are Stored & Synced

GitResume Agent manages a dual-tier storage system defined in your `gitresume.yaml`:

### 1. Primary Master Directory (`output.resume_dir`)
* The primary folder where your master `.docx` templates and compiled `.pdf` files are stored.
* Keeps all role-specific persona documents organized (e.g. `Forward_Deployed_Engineer.docx`, `GenAI_Engineer.docx`, `AI_Engineer.docx`, `Master_Resume.docx`).

### 2. Public Web / Portfolio Sync (`output.sync_paths`)
* Mirrors compiled `.docx` and `.pdf` files directly to your live portfolio website (e.g. `./portfolio_site/public/resume`), static site generator public folders, or CDN buckets.
* Every time you run `git-resume sync` (or make a git commit), your live portfolio immediately serves the freshest resumes.

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
# Option A: Ollama Cloud (Uses flagship cloud models without local download)
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_API_KEY=your_ollama_api_key

# Option B: Local Ollama (100% Free, Offline)
OLLAMA_BASE_URL=http://127.0.0.1:11434

# Option C: Google Gemini Free Endpoint
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🕹️ CLI Usage

### 1. Auto-Discover Schema from READMEs
Inspects configured repositories and syncs newly added tech tools or hackathon tags into `gitresume.yaml`:
```bash
git-resume auto-config
```

### 2. Install Zero-Touch Git Post-Commit Hooks
Automatically wires up post-commit hooks across all repositories listed in `gitresume.yaml`:
```bash
git-resume install-hooks
```

### 3. Live Codebase Intelligence Dashboard
Displays real-time commit counts, file statistics, total lines of code, and test suites across all tracked repositories:
```bash
git-resume scan
```

### 4. Synthesize Grounded Achievement Bullets
Uses multi-agent reasoning over recent git commits to generate role-specific Google XYZ bullets:
```bash
# Generate bullet for Forward-Deployed Engineer role
git-resume generate --repo MyProject --persona fde

# Generate bullet for Generative AI Engineer role
git-resume generate --repo MyProject --persona genai

# Generate bullet for AI/ML Engineer role
git-resume generate --repo MyProject --persona ai_engineer
```

### 5. Full End-to-End Multi-Agent Sync
Runs the entire pipeline (Inspect $\rightarrow$ Synthesize $\rightarrow$ Verify $\rightarrow$ Compile `.docx` $\rightarrow$ Export `.pdf` $\rightarrow$ Sync to Portfolio):
```bash
git-resume sync
```

---

## ⚙️ Configuration (`gitresume.yaml`)

```yaml
version: "1.0"

developer:
  name: "Your Name"
  email: "your.email@example.com"
  github: "https://github.com/yourusername"
  linkedin: "https://linkedin.com/in/yourprofile"
  location: "City, Country"

# Repositories to inspect & ground
repositories:
  - name: "EnterpriseAI"
    path: "./projects/EnterpriseAI"
    tag: "OpenAI Build Week Submission"
    primary_stack: ["Python", "FastAPI", "React", "TypeScript", "Qdrant", "PostgreSQL"]

  - name: "AgentOS"
    path: "./projects/AgentOS"
    tag: "Hackathon Track Submission"
    primary_stack: ["Python", "Google ADK", "LangGraph", "Next.js", "Firestore", "Google Cloud Run"]

# Resume Personas & Target Documents
personas:
  - id: "fde"
    title: "Agentic AI / Forward-Deployed Engineer"
    resume_file: "Your_Name_Agentic_AI_FDE_Resume.docx"
    emphasis: ["evals", "hybrid-search", "strict-abstention", "production-agents", "forward-deployed"]

  - id: "genai"
    title: "Generative AI Engineer"
    resume_file: "Your_Name_GenAI_Engineer_Resume.docx"
    emphasis: ["rag", "vector-embeddings", "langgraph", "llm-pipelines", "tool-calling"]

# Dual-Tier Storage & Compilation Targets
output:
  formats: ["docx", "pdf"]
  resume_dir: "./resumes"                     # Master storage directory
  sync_paths:
    - "./portfolio_site/public/resume"        # Public portfolio sync destination

# LLM Intelligence Engine
llm:
  provider: "ollama"
  model: "kimi-k2.7-code"
  fallback_model: "gpt-4o-mini"
```

---

## 🪝 Zero-Touch Git Hook Integration

How does the automation work on every commit?
When you run `git-resume install-hooks` (or `python scripts/install_hooks.py`):
1. It reads your configured repository paths in `gitresume.yaml`.
2. Locates each repository's `.git/hooks/` folder.
3. Installs an executable `post-commit` script that triggers `git-resume sync` in the background upon every commit.

```bash
git-resume install-hooks
```
*Output:*
```
🔧 Installing Git post-commit hooks...
  * ✓ Installed hook for [EnterpriseAI]: ./projects/EnterpriseAI
  * ✓ Installed hook for [AgentOS]: ./projects/AgentOS
✅ Successfully installed hooks across 2 repositories!
```

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

**Naman Manocha** — [@Naman6019](https://github.com/Naman6019)
