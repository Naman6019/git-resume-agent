# GitResume Agent 🚀

[![PyPI](https://img.shields.io/pypi/v/git-resume-agent.svg)](https://pypi.org/project/git-resume-agent/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CLI](https://img.shields.io/badge/CLI-Typer%20%26%20Rich-magenta.svg)](https://typer.tiangolo.com/)
[![Multi--Agent](https://img.shields.io/badge/Architecture-Autonomous%20Agentic%20Pipeline-orange.svg)](https://github.com/Naman6019/git-resume-agent)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20Cloud%20%7C%20Local-purple.svg)](https://ollama.com)
[![Tests](https://img.shields.io/badge/Tests-9%2F9%20Passing-brightgreen.svg)](tests/)
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
* **Scoped, Per-Repo Sync (opt-in)**: with `output.scoped_sync: true`, a commit in one tracked repo updates *only that project's section* of each resume — other projects' text, PDF exports, and pushes are left untouched. See [Scoped Sync](#-scoped-sync-update-only-the-project-that-changed).
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

### 1. Install via PyPI (Recommended)
```bash
pip install git-resume-agent
```

<details>
<summary><b>Or install from source (for contributors)</b></summary>

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

</details>

### 2. Initialize Starter Configuration
Scaffold a starter `gitresume.yaml` in your project folder with one command:
```bash
git-resume init
```
*(Creates a clean, annotated template ready for your projects, resume paths, and personas).*

### 3. Configure Environment (Optional LLM Keys)
Copy `.env.example` to `.env` (or set system environment variables):
```env
# Option A: Ollama Cloud (Uses flagship cloud models without local download)
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_API_KEY=your_ollama_api_key

# Option B: Local Ollama (100% Free, Offline)
OLLAMA_BASE_URL=http://127.0.0.1:11434

# Option C: Google Gemini Free Endpoint
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Wire Repositories & Enable Autonomy
```bash
# Detect tech stacks & tools automatically from repository READMEs & package manifests
git-resume auto-config

# Install zero-touch post-commit hooks across all tracked repositories
git-resume install-hooks

# Run first end-to-end resume sync
git-resume sync
```

---

## 🕹️ CLI Usage & Core Workflows

### 0. Generate Starter Configuration
Generate a starter `gitresume.yaml` configuration template in the current directory:
```bash
git-resume init
# Or specify a custom output path:
git-resume init --output ./my-config.yaml
```

### 1. Live Codebase Intelligence Dashboard
Displays real-time commit counts, file statistics, total lines of code, test suites, and deployment status across all tracked repositories:
```bash
git-resume scan
```
*Output:*
```
                     GitResume Live Codebase Intelligence                      
┌───────────┬───────────────────────────┬──────────────────────────────────┬─────────┬───────┬───────────┬─────────────┐
│ Repos     │ Tag / Track               │ Status & Links                   │ Commits │ Files │ Total LOC │ Test Suites │
├───────────┼───────────────────────────┼──────────────────────────────────┼─────────┼───────┼───────────┼─────────────┤
│ FundersAI │ OpenAI Build Week         │ ● Deployed (https://www.fund...  │     410 │   752 │   132,449 │         142 │
│           │                           │ https://github.com/...           │         │       │           │             │
│ TalentOS  │ All Things Agentic        │ ● Deployed (https://all-thin...  │      56 │   130 │    22,348 │          26 │
│           │                           │ https://github.com/...           │         │       │           │             │
│ CareFlow  │ Clinical Research         │ ○ In-Repo                        │       3 │    77 │    10,410 │           7 │
│           │                           │ https://github.com/...           │         │       │           │             │
│ GitResume │ Autonomous Multi-Agent... │ ○ In-Repo                        │      17 │    22 │     2,554 │           1 │
│           │                           │ https://github.com/...           │         │       │           │             │
└───────────┴───────────────────────────┴──────────────────────────────────┴─────────┴───────┴───────────┴─────────────┘
```

### 2. Auto-Discover Schema & Stack from READMEs
Inspects configured repositories, sanitizes code blocks, discovers git origin remotes, and syncs newly added tech tools or hackathon tags into `gitresume.yaml`:
```bash
git-resume auto-config
```

### 3. Full End-to-End Multi-Agent Sync (All Projects at Once)
Runs the entire multi-agent pipeline across all projects simultaneously (Inspect $\rightarrow$ Synthesize $\rightarrow$ Verify $\rightarrow$ Compile `.docx` with clickable hyperlinks $\rightarrow$ Export `.pdf` via Word COM $\rightarrow$ Sync to Portfolio):
```bash
git-resume sync
```

Pass `--repo` to scope this to a single project — only that repo's section of each
resume is rewritten, and only the resumes that actually changed are exported and
pushed (see [Scoped Sync](#-scoped-sync-update-only-the-project-that-changed)):
```bash
git-resume sync --repo FundersAI
```

### 4. Synthesize Grounded Achievement Bullets
Uses multi-agent reasoning over recent git commits to generate role-specific Google XYZ bullets:
```bash
# Generate bullet for Forward-Deployed Engineer role
git-resume generate --repo FundersAI --persona fde

# Generate bullet for Generative AI Engineer role
git-resume generate --repo TalentOS --persona genai

# Generate bullet for AI/ML Engineer role
git-resume generate --repo CareFlow --persona ai_engineer
```

### 5. Install Zero-Touch Git Post-Commit Hooks
Automatically wires up post-commit hooks across all repositories listed in `gitresume.yaml`:
```bash
git-resume install-hooks
```

### 6. Check & Propose Portfolio Description Updates
Checks tracked repos for README changes and opens a review PR against the portfolio site if a description looks stale (see [Keeping Portfolio Project Descriptions in Sync](#-keeping-portfolio-project-descriptions-in-sync)):
```bash
git-resume sync-descriptions
```

---

## 📝 Keeping Portfolio Project Descriptions in Sync

Resumes aren't the only thing that goes stale. The prose describing each
project on the portfolio site (`src/content/portfolio.ts`) drifts too, every
time a README gains a new capability, drops a limitation, or changes its
stack. `git-resume sync-descriptions` closes that loop, safely:

1. **Watches README.md, not every commit.** For each repository with a
   `portfolio_slug` set in `gitresume.yaml`, it checks whether `README.md` has
   a newer commit than the last time it looked (tracked in the local
   `.gitresume_state.json`, never committed).
2. **First sighting of a repo is a baseline, not a proposal.** The very first
   time a repository is checked there's nothing to diff against, so it just
   records the current README commit and moves on -- it never rewrites a
   description out of the blue on day one.
3. **Diffs, then judges.** On a real change, it feeds the README diff (plus
   the current site copy, for tone) to an LLM and asks a yes/no question
   first: is this change material enough to make the site copy stale? Typo
   fixes and badge shuffling get `NO_CHANGE`. A new capability, a changed
   boundary, or a stack change gets specific field-level rewrites.
4. **Grounds every claim before touching anything.** Any proposed sentence
   citing a number or stack item that doesn't actually appear in the README
   is dropped from the proposal. If everything gets dropped, nothing happens.
5. **Edits `portfolio.ts` field-by-field, never a blind overwrite.** The
   editor locates the exact object literal for the matching `slug` by
   brace-matching and replaces only the specific fields that changed,
   preserving formatting everywhere else.
6. **`npx tsc --noEmit` is the final gate.** The edited file is type-checked
   before anything is committed. A failure reverts the file on disk -- nothing
   broken ever reaches git.
7. **Opens a PR, never pushes to `main`.** A branch is cut from the
   portfolio's `base_branch`, the single file is committed and pushed, and a
   PR is opened via `gh pr create` with the README diff's context in the
   body. Netlify will build a deploy preview on it. Nothing reaches
   production without a human merging it.

Wire it into the same zero-touch loop as resume sync by adding
`portfolio_slug` (matching the `slug` in `portfolioProjects`) to a repo entry
and a `portfolio:` block pointing at the site:

```yaml
repositories:
  - name: MyNewProject
    portfolio_slug: my-new-project
    # ...

portfolio:
  repo_path: C:/Users/yourusername/Desktop/portfolio_site
  content_file: src/content/portfolio.ts
  base_branch: main
```

`git-resume install-hooks` wires this into the same post-commit hook as
resume sync, so a commit that changes a tracked repo's README triggers a
check automatically -- no separate hook to install.

---

## ➕ How to Add a New Repository to GitResume

Adding a new project to your resume pipeline takes less than 30 seconds:

### Step 1: Add the Repository to `gitresume.yaml`
Add an entry under the `repositories:` section:
```yaml
repositories:
  - name: MyNewProject
    path: C:/Users/yourusername/Desktop/MyNewProject
    repo_url: https://github.com/yourusername/MyNewProject   # Or leave blank for auto-discovery
    live_url: https://mynewproject.com                      # Optional (if deployed)
    deployed: true                                          # Set to true if live, false if in-repo
```

### Step 2: Auto-Discover Schema & Tools
Run `auto-config` to inspect the project's `README.md`, `package.json`, or `pyproject.toml` and populate tags and tools:
```bash
git-resume auto-config
```

### Step 3: Install Zero-Touch Git Hooks
Ensure background auto-sync is triggered every time you make a commit in the new repo:
```bash
git-resume install-hooks
```

### Step 4: Re-Sync Resumes
```bash
git-resume sync
```

---

## 📄 Managing Resume Length: 1-Page vs 2-Page Persona Strategy

When you have 4+ active repositories, fitting everything onto a single page without overcrowding is a common challenge. GitResume supports **Persona-Driven Project Budgeting (Strategy A)**:

```
                                  MASTER PIPELINE
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
     🎯 1-PAGE TARGETED RESUMES                      📑 2-PAGE MASTER RESUME
    (fde, genai, ai_engineer)                               (master)
 ┌───────────────────────────────┐               ┌───────────────────────────────┐
 │ • 2 Flagship Projects (Full)  │               │ • All 4+ Projects (Full)      │
 │   - FundersAI (3 bullets)     │               │   - FundersAI (4 bullets)     │
 │   - TalentOS (3 bullets)      │               │   - TalentOS (3 bullets)      │
 │ • Compact Secondary Projects  │               │   - CareFlow (3 bullets)      │
 │   - CareFlow & GitResume      │               │   - GitResume (3 bullets)     │
 │     (1-line in-repo links)    │               │                               │
 └───────────────────────────────┘               └───────────────────────────────┘
```

### 1. Targeted 1-Page Resumes (`fde`, `genai`, `ai_engineer`)
* **Flagship Focus**: Dedicate full multi-line accomplishment bullets to your top 2 relevant flagships (e.g. *FundersAI* and *TalentOS*).
* **Secondary / In-Progress Aggregation**: Mention non-flagship projects (e.g. *CareFlow*, *GitResume*) as a single compact, high-impact bullet with clickable in-repo links (`Repo: github.com/...`).
* **Bullet Count**: Maintain 3 bullets for primary work experience and 3 bullets per flagship project.

### 2. Comprehensive 2-Page Master Resume (`master`)
* **Full Coverage**: Dedicate full sections and 3–4 quantified bullets to every project in your portfolio (*FundersAI*, *TalentOS*, *CareFlow*, and *GitResume*).
* **Deep Architecture**: Include full infrastructure breakdowns, CI/CD pipeline counts, and test suite metrics.

---

## 🔗 Clickable Native Word & PDF Hyperlinks

GitResume Agent automatically embeds native Word OpenPackaging XML hyperlinks (`w:hyperlink` elements) into `.docx` documents:

* **Deployed Projects**: Subheaders feature clickable **Live** and **Repo** links (e.g. `Live: www.fundersai.co.in | Repo: github.com/Naman6019/FundersAI`).
* **Non-Deployed Projects**: Subheaders feature clickable **In-Repo** links (e.g. `Repo: github.com/Naman6019/CareFlow-Intelligence`).
* **PDF Preservation**: When Word COM exports the `.pdf` during `git-resume sync`, all hyperlinks remain interactive across web browsers, PDF viewers, and ATS portals.

---

## ⚙️ Configuration (`gitresume.yaml`)

### 🔍 How GitResume Locates Your Configuration
You do not need to manually specify the configuration path for every command. GitResume automatically locates `gitresume.yaml` using a multi-layer fallback search:
1. **Current Working Directory**: `./gitresume.yaml` or `./.gitresume.yaml`
2. **Parent Directories**: Automatically traverses upward to locate `gitresume.yaml` anywhere in your workspace.
3. **Environment Variable**: `GITRESUME_CONFIG=/path/to/gitresume.yaml`
4. **Git Repository Config**: `git config gitresume.config /path/to/gitresume.yaml` (registered automatically during `install-hooks`).
5. **User Home Directory**: `~/.config/git-resume/gitresume.yaml` or `~/.gitresume.yaml`
6. **CLI Override**: Pass `--config-path` / `-c` to any command.

---

### 🟢 Minimal Starter Configuration
Run `git-resume init` to generate this starter configuration automatically, or create `gitresume.yaml` manually:

```yaml
version: "1.0"

# [REQUIRED] Developer profile information
developer:
  name: "Your Name"
  email: "you@example.com"
  github: "https://github.com/yourusername"
  linkedin: "https://linkedin.com/in/yourprofile"  # [Optional]
  location: "San Francisco, CA"                   # [Optional]

# [REQUIRED] Repositories to inspect, ground, and track
repositories:
  - name: MyProject                               # [Required] Display name
    path: ./projects/my-project                   # [Required] Absolute path or relative to gitresume.yaml
    tag: Full-Stack Web Application               # [Optional] Hackathon track, badge, or subtitle
    repo_url: https://github.com/user/my-project  # [Optional] GitHub repository URL
    live_url: https://myproject.com              # [Optional] Live deployment link (if deployed)
    deployed: true                               # [Optional] true if live, false if in-repo
    primary_stack:                               # [Optional] Auto-populated via `git-resume auto-config`
      - Python
      - FastAPI
      - React
      - TypeScript

# [REQUIRED] Target resumes to compile (Word .docx files in output.resume_dir)
personas:
  - id: fullstack
    title: Full-Stack Software Engineer
    resume_file: FullStack_Resume.docx           # Master template filename inside output.resume_dir
    emphasis:
      - full-stack
      - distributed-systems
      - cloud

# [REQUIRED] Dual-Tier Storage & Compilation Targets
output:
  formats:
    - docx
    - pdf
  resume_dir: ./resumes                          # [Required] Folder containing master .docx templates
  sync_paths:                                    # [Optional] Public web/portfolio folders to mirror to
    - ./portfolio_site/public/resume
  scoped_sync: false                             # [Optional] Only update changed repo's section (default: false)

# [OPTIONAL] LLM Intelligence Engine for achievement bullet synthesis
llm:
  provider: ollama                               # ollama | openai | gemini (default: ollama)
  model: qwen2.5-coder:7b                        # or kimi-k2.7-code, deepseek-v4-pro, gpt-4o-mini
  fallback_model: gpt-4o-mini
```

---

### 📑 Production Multi-Persona Reference Configuration
The following reference shows a multi-repo, multi-persona production setup with 1-page targeted resumes and a 2-page master resume:

```yaml
version: "1.0"

developer:
  name: "Naman Manocha"
  email: "namanmanocha6019@gmail.com"
  github: "https://github.com/Naman6019"
  linkedin: "https://linkedin.com/in/naman-d-manocha"
  location: "Mumbai, India"

# Repositories to inspect & ground
repositories:
  - name: FundersAI
    path: C:/Users/naman/OneDrive/Desktop/FundersAI
    tag: OpenAI Build Week Submission
    repo_url: https://github.com/Naman6019/FundersAI
    live_url: https://www.fundersai.co.in
    deployed: true
    primary_stack:
      - Python
      - FastAPI
      - React
      - TypeScript
      - Qdrant
      - PostgreSQL
      - Next.js
      - LangGraph

  - name: TalentOS
    path: C:/Users/naman/OneDrive/Desktop/ALLThingsAgentic
    tag: All Things Agentic Hackathon (Taskmaster Track)
    repo_url: https://github.com/Naman6019/all-things-agentic
    live_url: https://all-things-agentic--allthingsagentic-505213.asia-southeast1.hosted.app
    deployed: true
    primary_stack:
      - Python
      - Google ADK
      - LangGraph
      - Next.js
      - Firestore
      - Google Cloud Run

  - name: CareFlow
    path: C:/Users/naman/OneDrive/Desktop/CareFlow Intelligence
    tag: Clinical Research Intelligence
    repo_url: https://github.com/Naman6019/CareFlow-Intelligence
    deployed: false
    primary_stack:
      - Python
      - FastAPI
      - Next.js
      - TypeScript
      - ChromaDB

  - name: GitResume
    path: C:/Users/naman/OneDrive/Desktop/resume_automation
    tag: Autonomous Multi-Agent Resume & Portfolio Intelligence Engine
    repo_url: https://github.com/Naman6019/git-resume-agent
    deployed: false
    primary_stack:
      - Python
      - Typer
      - Rich
      - Ollama
      - Pytest
      - python-docx

# Resume Personas & Target Documents
personas:
  - id: fde
    title: Agentic AI / Forward-Deployed Engineer (1 Page)
    resume_file: Naman_Manocha_Agentic_AI_FDE_Resume.docx
    emphasis:
      - evals
      - hybrid-search
      - strict-abstention
      - production-agents
      - forward-deployed

  - id: genai
    title: Generative AI Engineer (1 Page)
    resume_file: Naman_Manocha_GenAI_Engineer_Resume.docx
    emphasis:
      - rag
      - vector-embeddings
      - langgraph
      - llm-pipelines
      - tool-calling

  - id: ai_engineer
    title: AI / ML Engineer (1 Page)
    resume_file: Naman_Manocha_AI_Engineer_Resume.docx
    emphasis:
      - mlops
      - benchmarks
      - latency-optimization
      - fine-tuning
      - rag-systems

  - id: master_1page
    title: Master Resume (1 Page)
    resume_file: Naman_Manocha_Master_1Page_Resume.docx
    emphasis:
      - full-stack
      - ai-agents
      - rag
      - applied-ml
      - production-systems

  - id: master
    title: Master Comprehensive Resume (2 Page)
    resume_file: Naman_Manocha_Master_Resume.docx
    emphasis:
      - full-stack
      - distributed-systems
      - ai-agents
      - production-architecture

# Dual-Tier Storage & Compilation Targets
output:
  formats:
    - docx
    - pdf
  resume_dir: C:/Users/naman/OneDrive/Desktop/Personal/Resume
  sync_paths:
    - C:/Users/naman/OneDrive/Desktop/Personal/portfolio_site/public/resume
  # Opt-in: makes `install-hooks` write per-repo hooks so a commit in one repo only
  # updates/exports/pushes that project's section. See "Scoped Sync" below. Default: false.
  scoped_sync: false

# LLM Intelligence Engine
llm:
  provider: ollama
  model: kimi-k2.7-code
  fallback_model: gpt-4o-mini
```

---

## 🪝 Zero-Touch Git Hook Integration

### How It Works Under the Hood
When you run `git-resume install-hooks`:
1. It reads your configured repository paths in `gitresume.yaml`.
2. Locates each repository's `.git/hooks/` folder.
3. Installs an executable `post-commit` script that triggers `git-resume sync` in the background upon every commit (plus `sync-descriptions` to keep portfolio prose in sync with READMEs).
4. Sets `git config gitresume.config <path>` inside each tracked repository so `git-resume` always knows where to find its master configuration, no matter where git was executed.

### CLI Hook Commands:
```bash
# 1. Preview hook status and git remotes across all repositories without installing:
git-resume install-hooks --list

# 2. Install hooks across all repositories defined in gitresume.yaml:
git-resume install-hooks

# 3. Install a hook for one specific repository (by name or path):
git-resume install-hooks --repo MyProject
```

*Output:*
```
🔧 Installing Git post-commit hooks...
  * ✓ Installed hook & registered config for [EnterpriseAI]: ./projects/EnterpriseAI
  * ✓ Installed hook & registered config for [AgentOS]: ./projects/AgentOS
✅ Successfully configured hooks across 2 repositories!
```

---

## 🎯 Scoped Sync: Update Only the Project That Changed

By default, a commit in *any* tracked repo runs a full `sync`: every project's
section is re-inspected and rewritten in every persona resume, every PDF is
re-exported via Word COM, and every synced file is re-pushed — even if only one
repo actually changed. That's fine for a handful of projects, but it means a
commit in a repo nobody's resume-reads about still pays for a full Word export
and push cycle.

Set `output.scoped_sync: true` in `gitresume.yaml` and re-run `install-hooks` to
make each repo's hook self-scoped instead:

```yaml
output:
  scoped_sync: true
```
```bash
git-resume install-hooks   # regenerates hooks to pass --repo <name>
```

Each repo's `post-commit` hook now runs `git-resume sync --repo "<RepoName>"`
instead of a bare `sync`. A commit in `FundersAI`:
1. Still inspects every repo's live git stats (cheap — no LLM calls, no Word) so
   personas that blend two projects into one sentence (e.g. `genai`/`ai_engineer`,
   which mention TalentOS and GitResume in the same paragraph) stay correct.
2. Rewrites **only** the paragraph(s) that mention FundersAI in each persona resume
   — TalentOS, CareFlow, and GitResume's text are left byte-for-byte as they were.
3. PDF-exports **only** the resumes that were actually rewritten (skipped entirely
   if a persona never mentions FundersAI), instead of every `.docx` in `resume_dir`.
4. Copies and pushes **only** those changed docx/pdf files to `output.sync_paths`,
   instead of the whole directory.

`scoped_sync` is off by default — existing setups keep today's full-sync-on-every-commit
behavior until you opt in. You can also invoke it manually without touching the
config flag at all:
```bash
git-resume sync --repo TalentOS
```

---

## 🧪 Testing

Run the automated unit test suite:
```bash
pytest tests/ -v
```
```
collected 9 items
tests/test_git_resume.py::test_load_config PASSED                         [ 11%]
tests/test_git_resume.py::test_inspector_agent PASSED                     [ 22%]
tests/test_git_resume.py::test_grounding_verifier PASSED                  [ 33%]
tests/test_git_resume.py::test_synthesizer_agent PASSED                   [ 44%]
tests/test_git_resume.py::test_schema_discoverer PASSED                   [ 55%]
tests/test_git_resume.py::test_find_config_path_and_git_utils PASSED      [ 66%]
tests/test_git_resume.py::test_master_personas_config_and_compiler PASSED [ 77%]
tests/test_git_resume.py::test_scoped_update_resume PASSED                [ 88%]
tests/test_git_resume.py::test_init_command PASSED                        [100%]
====================== 9 passed in 1.41s ======================
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👤 Author

**Naman Manocha** — [@Naman6019](https://github.com/Naman6019)
