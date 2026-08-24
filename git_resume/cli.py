import os
import shutil
import sys
import typer
from rich.console import Console
from rich.table import Table

from git_resume.config import load_config
from git_resume.agents.inspector import InspectorAgent
from git_resume.agents.synthesizer import SynthesizerAgent
from git_resume.compilers.docx_compiler import DocxCompiler
from git_resume.compilers.pdf_compiler import PdfCompiler

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

app = typer.Typer(help="GitResume AI — Autonomous Multi-Agent Resume & Portfolio Intelligence Engine")
console = Console()

@app.command()
def scan(config_path: str = "gitresume.yaml"):
    """Scan configured Git repositories and display real-time engineering metrics."""
    config = load_config(config_path)
    inspector = InspectorAgent()
    
    table = Table(title="GitResume Live Codebase Intelligence", show_header=True, header_style="bold magenta")
    table.add_column("Repository", style="bold cyan")
    table.add_column("Tag / Track", style="yellow")
    table.add_column("Commits", justify="right")
    table.add_column("Files", justify="right")
    table.add_column("Total LOC", justify="right", style="green")
    table.add_column("Test Suites", justify="right", style="magenta")

    stats = inspector.inspect_all(config.repositories)
    for name, st in stats.items():
        table.add_row(
            name,
            str(st.get("tag", "")),
            str(st.get("commits", 0)),
            str(st.get("files", 0)),
            f"{st.get('loc', 0):,}",
            str(st.get("test_suites", 0))
        )

    console.print(table)

@app.command()
def sync(config_path: str = "gitresume.yaml"):
    """Run the end-to-end multi-agent pipeline: Inspect -> Synthesize -> Verify -> Compile -> Sync."""
    console.print("[bold blue]Starting GitResume Multi-Agent Sync...[/bold blue]")
    config = load_config(config_path)
    inspector = InspectorAgent()
    docx_compiler = DocxCompiler()
    pdf_compiler = PdfCompiler()

    # 1. Inspect
    stats = inspector.inspect_all(config.repositories)
    for name, st in stats.items():
        console.print(f"  * Inspected [cyan]{name}[/cyan]: {st['commits']} commits, {st['loc']:,} LOC, {st['test_suites']} test suites")

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
