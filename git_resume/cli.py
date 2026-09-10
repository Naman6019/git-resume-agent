import os
import shutil
import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from typing import Optional
from git_resume.config import load_config, find_config_path
from git_resume.agents.inspector import InspectorAgent
from git_resume.agents.synthesizer import SynthesizerAgent
from git_resume.agents.verifier import GroundingVerifierAgent
from git_resume.agents.schema_discoverer import SchemaDiscoverer
from git_resume.compilers.docx_compiler import DocxCompiler
from git_resume.compilers.pdf_compiler import PdfCompiler
from git_resume.utils.llm_client import LLMClient
from git_resume.utils.git_utils import (
    is_git_repo,
    get_git_remote_details,
    set_git_config,
    commit_and_push,
    get_last_commit_touching,
    get_file_diff,
    get_file_at_commit,
    open_portfolio_pr,
)
from git_resume.utils.state import state_path_for, load_state, save_state
from git_resume.agents.portfolio_writer import PortfolioDescriptionAgent
from git_resume.compilers.portfolio_ts_editor import apply_field_updates, validate_typescript, ProjectBlockNotFound

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

app = typer.Typer(help="GitResume AI — Autonomous Multi-Agent Resume & Portfolio Intelligence Engine")
console = Console()

@app.command()
def auto_config(config_path: str = "gitresume.yaml"):
    """Auto-discover project tracks, tags, and tech stack from README.md & manifests, updating gitresume.yaml."""
    discoverer = SchemaDiscoverer()
    console.print(f"[bold blue]🔍 Scanning repository READMEs and manifests for schema changes...[/bold blue]")
    updated, changes = discoverer.auto_sync_yaml(config_path)
    if updated:
        console.print(f"[bold green]✓ Auto-synced {config_path} successfully with repository changes:[/bold green]")
        for change in changes:
            console.print(f"  * [yellow]{change}[/yellow]")
    else:
        console.print(f"[bold green]✓ Configuration is already in sync with all repository READMEs and manifests.[/bold green]")

@app.command()
def install_hooks(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Install hook for a specific repository (by name or path)"),
    list_repos: bool = typer.Option(False, "--list", "-l", help="List all repositories with Git/GitHub status and hook state without installing"),
    config_path: str = typer.Option("gitresume.yaml", "--config-path", "-c", help="Path to gitresume.yaml configuration")
):
    """Install automated Git post-commit hooks across all or specific repositories in gitresume.yaml."""
    try:
        abs_config = find_config_path(config_path)
    except Exception as e:
        console.print(f"[red]Error locating configuration: {e}[/red]")
        raise typer.Exit(1)

    config = load_config(abs_config)

    # 1. Inspect and List mode
    if list_repos:
        table = Table(title="GitResume Repository Git/GitHub & Hook Inspection", show_header=True, header_style="bold magenta")
        table.add_column("Repository", style="bold cyan")
        table.add_column("Git Status", justify="center")
        table.add_column("GitHub / Remote", style="cyan")
        table.add_column("Hook Status", justify="center")
        table.add_column("Local Path", style="dim")

        for r in config.repositories:
            is_git = is_git_repo(r.path)
            remote_info = get_git_remote_details(r.path)
            
            git_badge = "[green]✓ Git Initialized[/green]" if is_git else "[red]✗ No .git[/red]"
            
            if remote_info["is_github"]:
                remote_badge = f"[bold green]GitHub[/bold green] ({remote_info['repo_identifier'] or remote_info['remote_url']})"
            elif remote_info["has_remote"]:
                remote_badge = f"[cyan]Remote[/cyan] ({remote_info['remote_url']})"
            else:
                remote_badge = "[yellow]○ Local only (No remote)[/yellow]" if is_git else "[dim]N/A[/dim]"

            hook_file = os.path.join(r.path, ".git", "hooks", "post-commit") if is_git else None
            hook_installed = os.path.exists(hook_file) if hook_file else False
            hook_badge = "[green]✓ Installed[/green]" if hook_installed else "[yellow]○ Not installed[/yellow]"

            table.add_row(r.name, git_badge, remote_badge, hook_badge, r.path)

        console.print(table)
        console.print(f"\n[dim]Config source: {abs_config}[/dim]")
        console.print("[dim]Tip: Use `git-resume install-hooks --repo <name>` to install a hook for a specific repo.[/dim]")
        return

    # 2. Filter target repos
    targets = config.repositories
    if repo:
        repo_lower = repo.lower().strip()
        targets = [
            r for r in config.repositories 
            if r.name.lower() == repo_lower or os.path.abspath(r.path).lower() == os.path.abspath(repo).lower()
        ]
        if not targets:
            console.print(f"[red]Error: Repository '{repo}' not found in {abs_config}[/red]")
            console.print(f"[dim]Configured repositories: {', '.join(r.name for r in config.repositories)}[/dim]")
            raise typer.Exit(1)

    console.print(f"[bold blue]🔧 Installing Git post-commit hooks using config [cyan]{abs_config}[/cyan]...[/bold blue]")
    
    hook_content = """#!/bin/sh
# GitResume AI: Auto-sync resume statistics after commit
git-resume sync || python -m git_resume.cli sync || true
# GitResume AI: Check for README changes worth reflecting on the portfolio site
git-resume sync-descriptions || python -m git_resume.cli sync-descriptions || true
"""
    installed = 0
    for target in targets:
        if not is_git_repo(target.path):
            console.print(f"  * [yellow]⚠ Skipped [{target.name}][/yellow]: No Git repository initialized at {target.path}")
            continue

        git_dir = os.path.join(target.path, ".git")
        hooks_dir = os.path.join(git_dir, "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        hook_path = os.path.join(hooks_dir, "post-commit")

        with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(hook_content)

        try:
            os.chmod(hook_path, 0o755)
        except Exception:
            pass

        # Register git config gitresume.config in target repo
        normalized_config_path = abs_config.replace("\\", "/")
        set_git_config(target.path, "gitresume.config", normalized_config_path)

        remote_info = get_git_remote_details(target.path)
        remote_tag = f" [cyan]({remote_info['remote_url']})[/cyan]" if remote_info.get("remote_url") else ""
        console.print(f"  * [green]✓ Installed hook & registered config for [{target.name}][/green]{remote_tag}: {target.path}")
        installed += 1

    if installed > 0:
        console.print(f"[bold green]✅ Successfully configured hooks for {installed} {'repository' if installed == 1 else 'repositories'}![/bold green]")
    else:
        console.print("[yellow]⚠ No hooks were installed. Make sure targeted repository has `git init` run.[/yellow]")

@app.command()
def scan(config_path: str = "gitresume.yaml", auto_update: bool = True):
    """Scan configured Git repositories and display real-time engineering metrics."""
    if auto_update:
        discoverer = SchemaDiscoverer()
        updated, changes = discoverer.auto_sync_yaml(config_path)
        if updated:
            console.print(f"[bold yellow]⚡ Auto-updated {config_path} from README changes:[/bold yellow]")
            for c in changes:
                console.print(f"  * {c}")

    config = load_config(config_path)
    inspector = InspectorAgent()
    
    table = Table(title="GitResume Live Codebase Intelligence", show_header=True, header_style="bold magenta")
    table.add_column("Repository", style="bold cyan")
    table.add_column("Tag / Track", style="yellow")
    table.add_column("Status & Links", style="cyan")
    table.add_column("Commits", justify="right")
    table.add_column("Files", justify="right")
    table.add_column("Total LOC", justify="right", style="green")
    table.add_column("Test Suites", justify="right", style="magenta")

    stats = inspector.inspect_all(config.repositories)
    for name, st in stats.items():
        is_dep = st.get("deployed", False)
        live = st.get("live_url")
        repo = st.get("repo_url")
        
        status_lines = []
        if is_dep and live:
            status_lines.append(f"[green]● Deployed[/green] ({live})")
        else:
            status_lines.append("[yellow]○ In-Repo[/yellow]")
            
        if repo:
            status_lines.append(f"[dim]{repo}[/dim]")
            
        links_display = "\n".join(status_lines) if status_lines else "[dim]No links[/dim]"

        table.add_row(
            name,
            str(st.get("tag", "")),
            links_display,
            str(st.get("commits", 0)),
            str(st.get("files", 0)),
            f"{st.get('loc', 0):,}",
            str(st.get("test_suites", 0))
        )

    console.print(table)

@app.command()
def generate(
    repo: str = typer.Option("FundersAI", help="Repository name to analyze"),
    persona: str = typer.Option("fde", help="Target persona ID (fde, genai, ai_engineer)"),
    config_path: str = "gitresume.yaml"
):
    """Autonomous Agentic Generation: Synthesizes a fresh, grounded bullet from recent git diffs."""
    discoverer = SchemaDiscoverer()
    discoverer.auto_sync_yaml(config_path)

    config = load_config(config_path)
    inspector = InspectorAgent()
    llm = LLMClient(provider=config.llm.provider, model=config.llm.model, fallback_model=config.llm.fallback_model)
    synthesizer = SynthesizerAgent(llm_client=llm)

    target_repo = next((r for r in config.repositories if r.name.lower() == repo.lower()), None)
    if not target_repo:
        console.print(f"[red]Error: Repository '{repo}' not found in {config_path}[/red]")
        raise typer.Exit(1)

    target_persona = next((p for p in config.personas if p.id.lower() == persona.lower()), None)
    emphasis = target_persona.emphasis if target_persona else ["full-stack", "architecture"]

    console.print(f"[bold blue]Multi-Agent Analysis for [cyan]{target_repo.name}[/cyan] (Persona: [yellow]{persona}[/yellow])...[/bold blue]")
    
    # 1. Inspect
    repo_data = inspector.inspect_repo(target_repo)
    console.print(f"  * Inspected {repo_data['commits']} commits, {repo_data['files']} files, {repo_data['loc']:,} LOC")

    # 2. Synthesize with LLM
    console.print("  * Synthesizer Agent reasoning over git commits & AST diffs...")
    result = synthesizer.generate_ai_bullet(repo_data, emphasis)

    # 3. Display
    status_badge = "[bold green][VERIFIED GROUNDED][/bold green]" if result["verified"] else "[bold yellow][UNVERIFIED][/bold yellow]"
    link_info = f"\n[cyan]{repo_data.get('formatted_links')}[/cyan]" if repo_data.get("formatted_links") else ""
    panel_body = f"[bold white]{result['bullet']}[/bold white]{link_info}\n\n{status_badge} [dim]{result['verification_note']}[/dim]"
    
    console.print("=" * 60)
    console.print(Panel(
        panel_body,
        title=f"Generated Achievement for {target_repo.name} ({target_persona.title if target_persona else persona})",
        subtitle=repo_data.get("formatted_links", ""),
        border_style="green" if result["verified"] else "yellow"
    ))

@app.command()
def sync(config_path: str = "gitresume.yaml", auto_update: bool = True):
    """Run the end-to-end multi-agent pipeline: Inspect -> Synthesize -> Verify -> Compile -> Sync."""
    if auto_update:
        discoverer = SchemaDiscoverer()
        updated, changes = discoverer.auto_sync_yaml(config_path)
        if updated:
            console.print(f"[bold yellow]⚡ Auto-synced {config_path} with repository READMEs:[/bold yellow]")
            for c in changes:
                console.print(f"  * {c}")

    console.print("[bold blue]Starting GitResume Multi-Agent Sync...[/bold blue]")
    config = load_config(config_path)
    inspector = InspectorAgent()
    docx_compiler = DocxCompiler()
    pdf_compiler = PdfCompiler()

    # 1. Inspect
    stats = inspector.inspect_all(config.repositories)
    for name, st in stats.items():
        links_str = f" [{st.get('formatted_links')}]" if st.get("formatted_links") else ""
        console.print(f"  * Inspected [cyan]{name}[/cyan]{links_str}: {st['commits']} commits, {st['loc']:,} LOC, {st['test_suites']} test suites")

    # 2. Update DOCX Personas
    console.print("[bold green]Updating Persona Resumes (.docx)...[/bold green]")
    for persona in config.personas:
        doc_path = os.path.join(config.output.resume_dir, persona.resume_file)
        if docx_compiler.update_resume(doc_path, persona.id, stats, developer_location=config.developer.location):
            console.print(f"  * Updated persona: [bold cyan]{persona.title}[/bold cyan] ({persona.resume_file})")

    # 3. Export PDFs
    console.print("[bold yellow]Compiling fresh PDFs via MS Word...[/bold yellow]")
    pdf_compiler.export_all(config.output.resume_dir)
    console.print("  * All PDF variants compiled.")

    # 4. Sync to Destinations
    console.print("[bold magenta]Syncing to Portfolio & Web Destinations...[/bold magenta]")
    for dest in config.output.sync_paths:
        if os.path.exists(dest):
            for fname in os.listdir(config.output.resume_dir):
                if (fname.endswith(".docx") or fname.endswith(".pdf")) and not fname.startswith("~$"):
                    shutil.copy2(os.path.join(config.output.resume_dir, fname), os.path.join(dest, fname))
                    console.print(f"  * Synced {fname} -> {dest}")

    # 5. Commit & Push each destination that is itself a Git repo, so hosts
    # like Netlify/Vercel pick up the fresh resumes on their next deploy.
    if config.output.auto_push:
        console.print("[bold blue]Publishing synced resumes (commit + push)...[/bold blue]")
        for dest in config.output.sync_paths:
            repo_root = _find_repo_root(dest)
            if not repo_root:
                console.print(f"  * [dim]Skipped {dest}: not inside a Git repository.[/dim]")
                continue

            result = commit_and_push(
                repo_root,
                message="chore(resume): sync latest resume variants\n\nAuto-synced by GitResume Agent.",
                paths=[os.path.relpath(dest, repo_root)],
            )
            if result.get("skipped"):
                console.print(f"  * [dim]{repo_root}: {result.get('reason', 'nothing to publish')}.[/dim]")
            elif result.get("success"):
                n = len(result.get("files", []))
                console.print(f"  * [bold green]✓ Pushed {n} file(s) to {repo_root} (branch {result.get('branch')})[/bold green]")
            else:
                console.print(f"  * [bold red]✗ {repo_root}: {result.get('reason', 'commit/push failed')}[/bold red]")
                console.print("    [dim]Files were still copied locally; push them manually when ready.[/dim]")

    console.print("[bold green]GitResume Sync Completed Successfully![/bold green]")


def _find_repo_root(path: str) -> Optional[str]:
    """Walks upward from `path` to find the nearest enclosing Git repository root
    (the directory that actually contains `.git`, not just any path inside the tree)."""
    current = os.path.abspath(path)
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


@app.command(name="sync-descriptions")
def sync_descriptions(config_path: str = "gitresume.yaml"):
    """For each tracked repo with a `portfolio_slug`, check whether README.md
    changed since the last check; if the change looks material, propose an
    updated project description and open a PR against the portfolio site for
    human review. Never pushes directly -- see CHANGELOG for why."""
    abs_config = find_config_path(config_path)
    config = load_config(abs_config)

    if not config.portfolio:
        console.print("[yellow]No `portfolio:` section configured in gitresume.yaml -- nothing to do.[/yellow]")
        raise typer.Exit(0)

    tracked = [r for r in config.repositories if r.portfolio_slug]
    if not tracked:
        console.print("[yellow]No repositories have `portfolio_slug` set -- nothing to do.[/yellow]")
        raise typer.Exit(0)

    state_path = state_path_for(abs_config)
    state = load_state(state_path)
    agent = PortfolioDescriptionAgent(
        llm_client=LLMClient(provider=config.llm.provider, model=config.llm.model, fallback_model=config.llm.fallback_model)
    )

    portfolio_repo = config.portfolio.repo_path
    content_path = os.path.join(portfolio_repo, config.portfolio.content_file)

    console.print("[bold blue]Checking tracked repositories for README changes...[/bold blue]")

    for repo in tracked:
        latest_sha = get_last_commit_touching(repo.path, "README.md")
        if not latest_sha:
            console.print(f"  * [dim]{repo.name}: no README.md history, skipping.[/dim]")
            continue

        entry = state.get(repo.name, {})
        prev_sha = entry.get("readme_sha")

        if prev_sha is None:
            state[repo.name] = {"readme_sha": latest_sha}
            console.print(f"  * [cyan]{repo.name}: establishing baseline at {latest_sha[:7]} (no proposal on first run).[/cyan]")
            continue

        if prev_sha == latest_sha:
            console.print(f"  * [dim]{repo.name}: README unchanged since last check.[/dim]")
            continue

        console.print(f"  * [bold]{repo.name}[/bold]: README changed ({prev_sha[:7]} -> {latest_sha[:7]}), analyzing...")

        readme_text = get_file_at_commit(repo.path, latest_sha, "README.md")
        readme_diff = get_file_diff(repo.path, prev_sha, latest_sha, "README.md")

        if not os.path.exists(content_path):
            console.print(f"    [bold red]✗ Portfolio content file not found at {content_path}[/bold red]")
            continue
        with open(content_path, "r", encoding="utf-8") as f:
            portfolio_source = f.read()

        try:
            proposed = agent.propose(repo, readme_text, readme_diff, portfolio_source)
        except ProjectBlockNotFound as e:
            console.print(f"    [bold red]✗ {e}[/bold red]")
            state[repo.name] = {"readme_sha": latest_sha}
            continue

        if not proposed:
            console.print(f"    [dim]No description update warranted (or LLM unavailable).[/dim]")
            state[repo.name] = {"readme_sha": latest_sha}
            continue

        accepted_keys = agent.verify_grounded(proposed, readme_text)
        filtered = {k: proposed[k] for k in accepted_keys}
        dropped = set(proposed.keys()) - set(accepted_keys)
        if dropped:
            console.print(f"    [yellow]Dropped ungrounded field(s): {', '.join(dropped)}[/yellow]")

        if not filtered:
            console.print(f"    [yellow]Proposal failed grounding checks entirely -- skipped.[/yellow]")
            state[repo.name] = {"readme_sha": latest_sha}
            continue

        try:
            new_source = apply_field_updates(portfolio_source, repo.portfolio_slug, filtered)
        except ProjectBlockNotFound as e:
            console.print(f"    [bold red]✗ {e}[/bold red]")
            state[repo.name] = {"readme_sha": latest_sha}
            continue

        with open(content_path, "w", encoding="utf-8") as f:
            f.write(new_source)

        ok, message = validate_typescript(portfolio_repo)
        if not ok:
            with open(content_path, "w", encoding="utf-8") as f:
                f.write(portfolio_source)  # revert -- never leave a broken build on disk
            console.print(f"    [bold red]✗ tsc failed, reverted: {message}[/bold red]")
            state[repo.name] = {"readme_sha": latest_sha}
            continue

        readme_commit_msg = get_last_commit_touching(repo.path, "README.md")
        branch_name = f"resume-agent/update-{repo.portfolio_slug}-{latest_sha[:7]}"
        field_list = ", ".join(filtered.keys())
        pr_body = (
            f"Proposed by GitResume Agent after a README change in **{repo.name}**.\n\n"
            f"**Fields updated:** {field_list}\n\n"
            f"**Source README diff:** `{prev_sha[:7]}..{latest_sha[:7]}` in `{repo.repo_url or repo.path}`\n\n"
            "This is an AI-generated proposal grounded in the README above -- review the wording "
            "before merging, this does not auto-deploy."
        )

        result = open_portfolio_pr(
            portfolio_repo,
            base_branch=config.portfolio.base_branch,
            branch_name=branch_name,
            files=[config.portfolio.content_file],
            commit_message=f"content({repo.portfolio_slug}): sync description from README update\n\nSource: {repo.name}@{latest_sha[:7]}",
            pr_title=f"Update {repo.name} description from README changes",
            pr_body=pr_body,
        )

        if result.get("skipped"):
            console.print(f"    [dim]{result.get('reason')}[/dim]")
        elif result.get("success"):
            console.print(f"    [bold green]✓ Opened PR: {result.get('pr_url')}[/bold green]")
        else:
            console.print(f"    [bold red]✗ {result.get('reason')}[/bold red]")

        state[repo.name] = {"readme_sha": latest_sha}

    save_state(state_path, state)
    console.print("[bold green]Description sync check complete.[/bold green]")

if __name__ == "__main__":
    app()
