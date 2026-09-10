# Changelog

All notable changes to **GitResume Agent** (`git-resume-agent`) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.7.0] - 2026-09-10

### 🚀 Added
- **Scoped, per-repo sync** (`gitresume.yaml` → `output.scoped_sync`, default `false`): until now, committing in *any* tracked repo ran a full `git-resume sync` that re-inspected and rewrote every project's section in every persona resume, re-exported every PDF via Word COM, and re-pushed every synced file — regardless of which repo actually changed. With `scoped_sync: true`, `install-hooks` instead writes each repo's hook as `git-resume sync --repo "<name>"`, so a FundersAI commit only rewrites FundersAI's paragraph(s) in each resume, only PDF-exports the resumes that actually changed, and only pushes those files to the sync destinations. Repos other than the one that committed are left byte-for-byte untouched.
  - `sync` gained a `--repo` / `-r` option; used standalone (without the config flag) it works the same way for a manual one-off scoped run.
  - `DocxCompiler.update_resume()` gained an optional `target_repo` parameter — every project-specific paragraph write is now gated on it, and the file is only saved (return `True`) if something in it actually pertains to that repo.
  - `PdfCompiler` gained `export_files()`, exporting a specific list of `.docx` paths instead of everything in `resume_dir`.
  - Off by default: existing installs keep today's full-sync-on-every-commit behavior until `scoped_sync` is set to `true` and `install-hooks` is re-run.

---

## [0.6.1] - 2026-09-10

### 🛡️ Fixed
- **Resume auto-push over-staged**: the 0.5.0 auto-push used `git add -A` in the destination repo, which swept up *any* other uncommitted file sitting in that working tree (in practice: `tsconfig.tsbuildinfo`, a stray TS build cache, landed in a resume-sync commit on the first live run). `sync`'s auto-push now scopes `git add` to the specific sync destination directory (`os.path.relpath(dest, repo_root)`) instead of the whole repo.

---

## [0.6.0] - 2026-09-10

### 🚀 Added
- **`git-resume sync-descriptions`**: closes the same staleness gap for portfolio project *descriptions* that 0.5.0 closed for resumes. For each repo with a new `portfolio_slug` set in `gitresume.yaml`, checks whether `README.md` gained a new commit since last seen (tracked in a new, gitignored `.gitresume_state.json`), and if the change looks material, proposes updated `summary`/`problem`/`build`/`outcome`/`limitations`/`stack` fields for that project's entry in `portfolio.ts`.
- **`PortfolioDescriptionAgent`** (`git_resume/agents/portfolio_writer.py`): asks the LLM a yes/no question before anything else -- is this README diff material enough to make the site copy stale? -- then drops any proposed field that cites a number or stack item absent from the README (`verify_grounded()`). A response matching `LLMClient`'s known heuristic-fallback sentinel is treated as "no working LLM," never as a proposal.
- **Field-level, AST-free TypeScript editing** (`git_resume/compilers/portfolio_ts_editor.py`): locates a project's object literal in `portfolioProjects` by brace-matching on its `slug`, then replaces only the specific fields that changed via scoped regex + `json.dumps` escaping -- never a blind block overwrite. `validate_typescript()` runs `npx tsc --noEmit` as the final gate; a failure reverts the file on disk before anything is committed.
- **PR-only publishing for this path** (`open_portfolio_pr()` in `git_utils.py`): unlike resume sync's direct-to-`main` auto-push, description changes always land as a branch + `gh pr create`, deliberately -- these are AI-authored sentences about the developer's own work, and the resume auto-push precedent doesn't extend to unreviewed public site copy.
- **`portfolio_slug`** on `RepoConfig` and a new top-level **`portfolio:`** config block (`repo_path`, `content_file`, `base_branch`) in `config.py` / `gitresume.yaml`.
- The shared post-commit hook template (`cli.py` and `scripts/install_hooks.py`) now runs `sync-descriptions` alongside `sync`, so no separate hook install step is needed.

---

## [0.5.0] - 2026-09-10

### 🚀 Added
- **Auto-publish sync destinations**: `git-resume sync` previously stopped at `shutil.copy2()` into `output.sync_paths` — the freshest resumes sat as uncommitted changes in `portfolio_site` until someone noticed and pushed by hand, so hosts like Netlify never picked them up automatically. `sync` now walks each sync path up to its enclosing Git repo (`_find_repo_root()` in `cli.py`) and runs the new `commit_and_push()` (`git_utils.py`) there: stage, commit (`chore(resume): sync latest resume variants`), push to the current branch's `origin`. Fully closes the "edit a resume locally → live portfolio serves it" loop with no manual git step.
- **`output.auto_push` config flag** (`config.py`, default `true`): set to `false` in `gitresume.yaml` to keep the old copy-only behavior for a given setup.
- Push failures (no remote, rejected push, detached HEAD, etc.) are reported per-destination without failing the whole sync — files are still copied locally, and the message says push them manually.

---

## [0.4.0] - 2026-09-10

### 🚀 Added
- **1-Page Master Resume content expansion**: restored two bullets that the 1-page distillation had compressed out relative to the 2-page master — `FundersAI`'s "Cloud Storage & Billing" (Cloudflare R2, Razorpay) and `CareFlow`'s "Human-in-the-Loop Data Agent" (synthetic patient/encounter ingestion, OpenRouter fallback) — to use the whitespace left at the bottom of the page. Verified via headless LibreOffice conversion that the page count stays at exactly 1 with margin to spare.

### 🛡️ Refined & Improved
- **Compiler robustness for `master_1page`**: `DocxCompiler.update_resume()` previously located the FundersAI/TalentOS stat lines by a hardcoded paragraph index, which would silently start overwriting the wrong paragraph the next time the template gained or lost a paragraph (as the bullets above just did). Added `_find_stat_para()`, which locates each stat line relative to its project's header text instead, and switched the `master_1page` branch to use it (with the old index kept only as a last-resort fallback).
- **Header/location sync** (carried from the previous 0.3.x hotfix, now versioned): `sync_header_location()` keeps the resume's header city in sync with `developer.location` in `gitresume.yaml` on every persona/every sync, instead of that field being baked into the template and only ever set once by hand.
- **GitResume self-listing**: `sync` now lists the GitResume project itself on every persona (`sync_gitresume_block()` / `append_gitresume_to_paragraph()`), idempotently, instead of computing its stats and never using them.

### ⚠️ Known issue
- `scripts/build_scaffold.py` is a stale historical bootstrap script and has not been kept in sync with the live package (it predates `master_1page`, the GitResume repo entry, and several `git_utils`/`config` fields the current CLI depends on). It is not part of the normal `sync` flow, but running it would regress the package. It's been marked deprecated at the top of the file — do not rerun it. It should either be regenerated from the current package or deleted; ask before doing either since it's a real content change either way.

---

## [0.3.0] - 2026-09-05

### 🚀 Added
- **Dual Master Resume Suite (1-Page & 2-Page)**:
  - Added new generalist **1-Page Master Resume** (`Naman_Manocha_Master_1Page_Resume.docx` / `.pdf`): a balanced, high-density distillation of the master resume covering classical ML, multi-agent systems, citation-grounded RAG, cloud microservices, and product ownership without persona bias.
  - Engineered exact geometry (0.28" margins, calibrated line spacing, active hyperlinks) guaranteeing a strict **1-page ATS-ready PDF export**.
  - Registered `master_1page` persona in `gitresume.yaml`.
- **Compiler & Pipeline Integration**:
  - Enhanced `DocxCompiler.update_resume()` to dynamically support `master_1page` alongside `master` (2-page).
  - Updated `scripts/sync_resumes.py` to compile and sync both master resume variants.
  - Added test coverage in `tests/test_git_resume.py` validating both master configurations and compilers.

### 🛡️ Refined & Improved
- **2-Page Master Resume Pagination**:
  - Restructured page flow in `Naman_Manocha_Master_Resume.docx` with an explicit page break before `FundersAI Reports`, eliminating the orphaned header at the bottom of Page 1.
  - Page 1 now cleanly encapsulates Summary, Skills, PayGain experience, and FundersAI; Page 2 cleanly encapsulates FundersAI Reports, CareFlow Intelligence, TalentOS, SQuAD QA, and Education.
  - Verified strict **2-page ATS-ready PDF export** with zero spillover.
- **Developer Configuration**:
  - Updated developer email in `gitresume.yaml` to `namanmanocha42248@gmail.com`.

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
