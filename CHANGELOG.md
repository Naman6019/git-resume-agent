# Changelog

All notable changes to **GitResume Agent** (`git-resume-agent`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-08-25

### 🚀 Added
- **Dual-Link & In-Repo System**:
  - `RepoConfig` now natively supports `repo_url`, `live_url`, and `deployed` boolean flags.
  - Deployed projects automatically format and surface **both** live deployment links and GitHub repository links (`Live: ... | Repo: ...`).
  - In-progress and non-deployed projects automatically surface direct **in-repo links** (`Repo: https://github.com/...`) across resumes and dashboards.
- **Native Clickable Word & PDF Hyperlinks**:
  - Implemented OpenPackaging `w:hyperlink` XML generator in `DocxCompiler` allowing Word `.docx` documents and exported `.pdf` files to feature active, clickable links styled in standard blue (`#0066CC`) with underlines.
  - Added clean URL presentation to prevent text overflow while retaining complete URL destinations.
- **Automated Git Remote & README Link Discovery**:
  - Added `get_git_remote_url()` in `git_utils.py` to auto-extract and normalize SSH (`git@github.com:...`) and HTTPS git remotes into clean web URLs.
  - Enhanced `SchemaDiscoverer` to parse Markdown badges and links (`[Live App](...)`, `[Code Repository](...)`) from project `README.md` files.
- **Enhanced Codebase Intelligence CLI**:
  - Added dedicated **Status & Links** column to `git-resume scan` showing live deployment indicators (`● Deployed`) and in-repo indicators (`○ In-Repo`).
  - Added formatted links to `git-resume generate` panels and `git-resume sync` progress streams.
- **Expanded Test Suite**:
  - Added unit test coverage for `RepoConfig` link properties, `InspectorAgent` link enrichment, and `SchemaDiscoverer` URL extraction.

### 🛡️ Fixed & Improved
- **Code-Fence Sanitization**: `SchemaDiscoverer` now strips fenced code blocks (```` ```...``` ````) from READMEs prior to metadata extraction, preventing sample configuration snippets from overwriting actual project tags or stacks.
- **Word COM Stability**: Enhanced error recovery and process handling for Word COM PDF export automation.

---

## [0.1.0] - 2026-08-24

### 🌟 Initial Release
- **Perception Engine**: Zero-overhead git repository scanning (`commits`, `files`, `LOC`, `test_suites`) in < 5ms.
- **Schema Discovery Agent**: Automatic tech stack extraction from `package.json`, `pyproject.toml`, and `requirements.txt`.
- **Reasoning & Synthesis Agent**: Multi-agent LLM reasoning pipeline generating Google XYZ accomplishment bullets.
- **Adversarial Grounding Verifier**: AST-based verification eliminating metric hallucinations.
- **Docx & PDF Compiler**: In-place paragraph run modification preserving Word styles and exporting PDFs.
- **Multi-Persona System**: Support for role-tailored resumes (`fde`, `genai`, `ai_engineer`, `master`).
- **Zero-Touch Git Post-Commit Hooks**: Automated background synchronization on `git commit`.
- **Portfolio Mirroring**: Automatic syncing of compiled resumes directly to live web destinations.
