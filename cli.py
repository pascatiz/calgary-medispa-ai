#!/usr/bin/env python3
"""
Calgary MediSpa AI - Command Line Interface
Usage: python cli.py [command] [subcommand]
"""

import sys
import os
import click
from datetime import datetime
from pathlib import Path

# Ensure output and log directories exist
Path("outputs").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)


def log_action(action: str, status: str, message: str = ""):
    """Write a log entry to /logs/cli.log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{status.upper()}] {action}: {message}\n"
    log_path = Path("logs") / "cli.log"
    with open(log_path, "a") as f:
        f.write(log_line)
    return log_line.strip()


def safe_save(filepath: Path, content: str) -> bool:
    """Save content to file, prompting user if file already exists."""
    if filepath.exists():
        confirm = input(f"  File {filepath} already exists. Overwrite? (yes/no): ").strip().lower()
        if confirm not in ("yes", "y"):
            print(f"  Skipped: {filepath}")
            return False
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"  Saved: {filepath}")
    return True


@click.group()
def cli():
    """Calgary MediSpa AI Automation Command Centre"""
    pass


@cli.command()
@click.argument("module")
def run(module: str):
    """Run a specific automation module.

    \b
    Available modules:
      soap        Generate a SOAP clinical note
      payroll     Validate payroll CSV data
      training    Check injector training status
      marketing   Generate content calendar
      productivity  Run productivity planning tools
      obsidian    Manage the git-synced Obsidian vault
    """
    modules = {
        "soap": run_soap,
        "payroll": run_payroll,
        "training": run_training,
        "marketing": run_marketing,
        "productivity": run_productivity,
        "obsidian": run_obsidian,
    }

    if module not in modules:
        click.echo(f"  ERROR: Unknown module '{module}'")
        click.echo(f"  Available: {', '.join(modules.keys())}")
        log_action(f"run {module}", "error", "Unknown module")
        sys.exit(1)

    click.echo(f"\n  Calgary MediSpa AI — Running: {module.upper()}")
    click.echo("  " + "=" * 50)
    log_action(f"run {module}", "start", "Module launched")

    try:
        modules[module]()
        log_action(f"run {module}", "success", "Module completed")
    except KeyboardInterrupt:
        click.echo("\n  Interrupted by user.")
        log_action(f"run {module}", "interrupted", "User cancelled")
    except Exception as e:
        click.echo(f"\n  ERROR: {e}")
        log_action(f"run {module}", "error", str(e))
        sys.exit(1)


@cli.command()
def status():
    """Check system status and environment."""
    click.echo("\n  Calgary MediSpa AI — System Status")
    click.echo("  " + "=" * 50)

    checks = {
        "Python version": sys.version.split(" ")[0],
        "Working directory": os.getcwd(),
        "outputs/ directory": "OK" if Path("outputs").exists() else "MISSING — run mkdir outputs",
        "logs/ directory": "OK" if Path("logs").exists() else "MISSING — run mkdir logs",
        ".env file": "Found" if Path(".env").exists() else "Not found (copy .env.example to .env)",
    }

    for item, value in checks.items():
        status_icon = "OK" if "MISSING" not in str(value) and "Not found" not in str(value) else "WARN"
        click.echo(f"  [{status_icon}] {item}: {value}")

    # Count outputs
    outputs = list(Path("outputs").glob("*.md")) if Path("outputs").exists() else []
    click.echo(f"  [OK] Output files: {len(outputs)} .md files in /outputs")

    # Obsidian vault health
    vault = Path("vault")
    if vault.exists():
        notes = list(vault.rglob("*.md"))
        memory_ok = (vault / "90-Claude-Memory" / "Memory.md").exists()
        click.echo(f"  [OK] Obsidian vault: {len(notes)} notes in /vault")
        click.echo(f"  [{'OK' if memory_ok else 'WARN'}] Claude memory: "
                   f"{'Found' if memory_ok else 'MISSING — run: python cli.py recall'}")
        import subprocess
        unsynced = subprocess.run(
            ["git", "status", "--porcelain", "--", "vault"],
            capture_output=True, text=True).stdout.strip()
        if unsynced:
            count = len(unsynced.splitlines())
            click.echo(f"  [WARN] Vault sync: {count} unsynced change(s) — run: python cli.py sync")
        else:
            click.echo("  [OK] Vault sync: no uncommitted vault changes")
    else:
        click.echo("  [WARN] Obsidian vault: MISSING — run: python cli.py recall to create it")

    # Count logs
    log_file = Path("logs") / "cli.log"
    if log_file.exists():
        with open(log_file) as f:
            lines = f.readlines()
        click.echo(f"  [OK] Log entries: {len(lines)} entries in /logs/cli.log")
    else:
        click.echo("  [INFO] Log file: No log entries yet")

    log_action("status", "success", "Status check completed")
    click.echo("\n  System ready. Run: python cli.py run <module>\n")


@cli.command()
@click.option("--lines", default=20, help="Number of log lines to show (default: 20)")
def logs(lines: int):
    """View recent execution logs."""
    log_file = Path("logs") / "cli.log"

    if not log_file.exists():
        click.echo("\n  No logs found yet. Run a module first.\n")
        return

    click.echo(f"\n  Calgary MediSpa AI — Recent Logs (last {lines} entries)")
    click.echo("  " + "=" * 50)

    with open(log_file) as f:
        all_lines = f.readlines()

    recent = all_lines[-lines:]
    for line in recent:
        line = line.strip()
        if "[ERROR]" in line or "[WARN]" in line:
            click.echo(f"  WARN  {line}")
        elif "[SUCCESS]" in line:
            click.echo(f"  OK    {line}")
        else:
            click.echo(f"        {line}")

    click.echo(f"\n  Total log entries: {len(all_lines)}\n")


# ─────────────────────────────────────────────
# Obsidian vault commands
# ─────────────────────────────────────────────

@cli.command()
@click.argument("content")
@click.option("--title", default=None, help="Note title (default: first words of content)")
@click.option("--folder", default="00-Inbox", help="Vault folder (default: 00-Inbox)")
@click.option("--tags", default="", help="Comma-separated tags")
def note(content: str, title: str, folder: str, tags: str):
    """Save a quick note into the Obsidian vault.

    Example: python cli.py note "Restock filler order placed" --tags ops
    """
    from obsidian.vault_manager import add_note
    note_title = title or " ".join(content.split()[:6])
    tag_list = [t for t in tags.split(",") if t.strip()]
    filepath = add_note(note_title, content, folder=folder, tags=tag_list)
    click.echo(f"  Note saved: {filepath}")
    click.echo("  Run: python cli.py sync — to push it to your Obsidian app.")
    log_action("note", "success", str(filepath))


@cli.command()
@click.argument("entry")
@click.option("--section", default="Session Log",
              help="Memory section: Preferences, Clinic Facts, or Session Log")
def remember(entry: str, section: str):
    """Add an entry to Claude's persistent memory.

    Example: python cli.py remember "Prefers SOAP notes in bullet form" --section Preferences
    """
    from obsidian.vault_manager import remember as vault_remember
    filepath = vault_remember(entry, section=section)
    click.echo(f"  Remembered in: {filepath}")
    log_action("remember", "success", entry[:80])


@cli.command()
def recall():
    """Show Claude's persistent memory file."""
    from obsidian.vault_manager import recall as vault_recall
    click.echo("\n" + vault_recall())
    log_action("recall", "success", "Memory displayed")


@cli.command()
@click.option("-m", "--message", default=None, help="Commit message (default: auto-generated)")
def sync(message: str):
    """Commit and push vault/memory changes so they reach your Obsidian app.

    Run this after adding notes. Your Obsidian Git plugin (or a git pull on
    your computer) then picks them up automatically.
    """
    import subprocess

    def git(*args):
        return subprocess.run(["git", *args], capture_output=True, text=True)

    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if not branch or branch == "HEAD":
        click.echo("  ERROR: Not on a git branch — cannot sync.")
        log_action("sync", "error", "Detached HEAD or not a repo")
        sys.exit(1)

    git("add", "vault")
    staged = git("diff", "--cached", "--name-only").stdout.strip()
    if staged:
        count = len(staged.splitlines())
        msg = message or f"Vault sync: {count} note file(s) updated"
        commit = git("commit", "-m", msg)
        if commit.returncode != 0:
            click.echo(f"  ERROR: Commit failed:\n{commit.stderr or commit.stdout}")
            log_action("sync", "error", "Commit failed")
            sys.exit(1)
        click.echo(f"  Committed: {msg}")
    else:
        click.echo("  No new vault changes to commit.")

    pull = git("pull", "--rebase", "--autostash", "origin", branch)
    if pull.returncode != 0 and "couldn't find remote ref" not in (pull.stderr or "").lower():
        click.echo(f"  WARN: Pull failed (continuing to push):\n{(pull.stderr or '').strip()}")

    push = git("push", "-u", "origin", branch)
    if push.returncode != 0:
        click.echo(f"  ERROR: Push failed:\n{(push.stderr or '').strip()}")
        click.echo("  Your notes are committed locally — retry with: python cli.py sync")
        log_action("sync", "error", "Push failed")
        sys.exit(1)

    click.echo(f"  Synced to origin/{branch} — your Obsidian app will pick it up on next pull.")
    log_action("sync", "success", f"Pushed vault to {branch}")


@cli.command()
@click.argument("query")
def search(query: str):
    """Search all vault notes for a keyword."""
    from obsidian.vault_manager import search_notes, VAULT_DIR
    matches = search_notes(query)
    click.echo(f"\n  {len(matches)} notes matching '{query}':")
    for path in matches[:25]:
        click.echo(f"  - {path.relative_to(VAULT_DIR)}")
    log_action("search", "success", f"{query} -> {len(matches)} matches")


# ─────────────────────────────────────────────
# Module runners
# ─────────────────────────────────────────────

def run_soap():
    from soap.soap_generator import run
    run(safe_save)


def run_payroll():
    from payroll.payroll_validator import run
    run(safe_save)


def run_training():
    from training.injector_training_tracker import run
    run(safe_save)


def run_marketing():
    from marketing.content_pipeline import run
    run(safe_save)


def run_obsidian():
    from obsidian.vault_manager import run
    run(safe_save)


def run_productivity():
    from productivity.daily_planner import run as run_planner
    from productivity.meeting_notes import run as run_meetings
    from productivity.goal_tracker import run as run_goals

    click.echo("  Select productivity tool:")
    click.echo("  1. Daily Planner")
    click.echo("  2. Meeting Notes")
    click.echo("  3. Goal & KPI Tracker")
    click.echo("  4. Run all three")

    choice = input("  Enter choice (1-4): ").strip()

    if choice == "1":
        run_planner(safe_save)
    elif choice == "2":
        run_meetings(safe_save)
    elif choice == "3":
        run_goals(safe_save)
    elif choice == "4":
        run_planner(safe_save)
        run_meetings(safe_save)
        run_goals(safe_save)
    else:
        click.echo("  Invalid choice. Running daily planner by default.")
        run_planner(safe_save)


if __name__ == "__main__":
    cli()
