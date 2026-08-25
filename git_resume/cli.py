import os
import shutil
import sys
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from git_resume.config import load_config
from git_resume.agents.inspector import InspectorAgent
from git_resume.agents.synthesizer import SynthesizerAgent
from git_resume.agents.verifier import GroundingVerifierAgent
from git_resume.agents.schema_discoverer import SchemaDiscoverer
from git_resume.compilers.docx_compiler import DocxCompiler
from git_resume.compilers.pdf_compiler import PdfCompiler
from git_resume.utils.llm_client import LLMClient

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
        console.print(f"[bold green]✓ {config_path} is already in sync with all repository READMEs and manifests.[/bold green]")

@app.command()
def install_hooks(config_path: str = "gitresume.yaml"):
    """Install automated Git post-commit hooks across all repositories in gitresume.yaml."""
    config = load_config(config_path)
    console.print("[bold blue]🔧 Installing Git post-commit hooks...[/bold blue]")
    
    hook_content = """#!/bin/sh
# GitResume AI: Auto-sync resume statistics after commit
git-resume sync || python -m git_resume.cli sync || true
"""
    installed = 0
    for repo in config.repositories:
        git_dir = os.path.join(repo.path, ".git")
        hooks_dir = os.path.join(git_dir, "hooks")
        if os.path.exists(git_dir):
            os.makedirs(hooks_dir, exist_ok=True)
            hook_path = os.path.join(hooks_dir, "post-commit")
            with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(hook_content)
            try:
                os.chmod(hook_path, 0o755)
            except Exception:
                pass
            console.print(f"  * [green]✓ Installed hook for [{repo.name}][/green]: {repo.path}")
            installed += 1
        else:
            console.print(f"  * [yellow]⚠ Skipped [{repo.name}] (no .git directory at {repo.path})[/yellow]")

    console.print(f"[bold green]✅ Successfully installed hooks across {installed} repositories![/bold green]")

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
        if docx_compiler.update_resume(doc_path, persona.id, stats):
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

    console.print("[bold green]GitResume Sync Completed Successfully![/bold green]")

if __name__ == "__main__":
    app()
