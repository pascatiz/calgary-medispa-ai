#!/usr/bin/env python3
"""
Calgary MediSpa AI - Obsidian Vault Manager
Manages the git-synced Obsidian vault in /vault: quick note capture,
search, and Claude's persistent memory file.

The vault/ folder is a real Obsidian vault. Open it in the Obsidian app
(or sync it with the Obsidian Git community plugin) and every note saved
here appears on all your devices after a git push/pull.
"""

import click
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path("vault")
INBOX_FOLDER = "00-Inbox"
NOTES_FOLDER = "10-Notes"
OPERATIONS_FOLDER = "20-Clinic-Operations"
MEMORY_FOLDER = "90-Claude-Memory"
MEMORY_FILE = VAULT_DIR / MEMORY_FOLDER / "Memory.md"

VAULT_FOLDERS = [INBOX_FOLDER, NOTES_FOLDER, OPERATIONS_FOLDER, MEMORY_FOLDER]


def ensure_vault():
    """Create the vault folder structure if it does not exist yet."""
    for folder in VAULT_FOLDERS:
        (VAULT_DIR / folder).mkdir(parents=True, exist_ok=True)
    if not MEMORY_FILE.exists():
        MEMORY_FILE.write_text(
            "# Claude Memory\n\n"
            "Persistent memory for Claude Code sessions. Claude reads this file at the\n"
            "start of every session and appends dated entries as it learns.\n\n"
            "## Preferences\n\n"
            "## Clinic Facts\n\n"
            "## Session Log\n",
            encoding="utf-8",
        )


def slugify(title: str) -> str:
    """Turn a note title into a safe filename."""
    safe = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
    return safe.strip().replace(" ", "-")[:60] or "Untitled"


def build_note(title: str, content: str, tags=None, source: str = "cli") -> str:
    """Build note markdown with YAML frontmatter Obsidian understands."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    tag_list = tags or []
    lines = [
        "---",
        f"created: {now}",
        f"source: {source}",
        "tags:",
    ]
    lines.extend(f"  - {t.strip().lstrip('#')}" for t in tag_list if t.strip())
    lines.extend(["---", "", f"# {title}", "", content, ""])
    return "\n".join(lines)


def add_note(title: str, content: str, folder: str = INBOX_FOLDER,
             tags=None, source: str = "cli") -> Path:
    """Save a note into the vault and return its path."""
    ensure_vault()
    target_dir = VAULT_DIR / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    filepath = target_dir / f"{slugify(title)}.md"
    if filepath.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filepath = target_dir / f"{slugify(title)}-{stamp}.md"
    filepath.write_text(build_note(title, content, tags, source), encoding="utf-8")
    return filepath


def list_notes(folder: str = None):
    """List all notes in the vault (or one folder), newest first."""
    ensure_vault()
    base = VAULT_DIR / folder if folder else VAULT_DIR
    if not base.exists():
        return []
    notes = [p for p in base.rglob("*.md")]
    return sorted(notes, key=lambda p: p.stat().st_mtime, reverse=True)


def search_notes(query: str):
    """Case-insensitive search across note filenames and contents."""
    ensure_vault()
    query_lower = query.lower()
    matches = []
    for path in VAULT_DIR.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if query_lower in path.stem.lower() or query_lower in text.lower():
            matches.append(path)
    return sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)


def remember(entry: str, section: str = "Session Log") -> Path:
    """Append a dated entry to Claude's persistent memory file."""
    ensure_vault()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = MEMORY_FILE.read_text(encoding="utf-8")
    heading = f"## {section}"
    new_line = f"- **{now}** — {entry.strip()}"
    if heading in text:
        head, _, tail = text.partition(heading)
        # Insert newest entry at the top of the section, keeping the blank
        # line that follows the heading intact
        tail_lines = tail.split("\n")
        idx = 1
        while idx < len(tail_lines) and tail_lines[idx].strip() == "":
            idx += 1
        tail_lines.insert(idx, new_line)
        text = head + heading + "\n".join(tail_lines)
    else:
        text = text.rstrip() + f"\n\n{heading}\n{new_line}\n"
    MEMORY_FILE.write_text(text, encoding="utf-8")
    return MEMORY_FILE


def recall() -> str:
    """Return the full contents of Claude's memory file."""
    ensure_vault()
    return MEMORY_FILE.read_text(encoding="utf-8")


def get_multiline(prompt):
    click.echo(f"  {prompt} (type END on new line when done)")
    lines_in = []
    while True:
        try:
            line = input("  ")
            if line.strip().upper() == "END":
                break
            lines_in.append(line)
        except EOFError:
            break
    return "\n".join(lines_in) if lines_in else "[Empty note]"


def run(safe_save):
    """Interactive vault menu for `python cli.py run obsidian`."""
    ensure_vault()
    click.echo("\n  OBSIDIAN VAULT")
    click.echo("  Git-synced vault at /vault — open it in the Obsidian app.\n")
    click.echo("  1. Add a note to the Inbox")
    click.echo("  2. List recent notes")
    click.echo("  3. Search notes")
    click.echo("  4. View Claude memory")
    click.echo("  5. Add to Claude memory")

    choice = input("  Enter choice (1-5): ").strip()

    if choice == "1":
        title = input("  Note title: ").strip() or "Quick Note"
        tags_raw = input("  Tags (comma-separated, optional): ").strip()
        tags = [t for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        content = get_multiline("\n  Note content:")
        path = add_note(title, content, tags=tags)
        click.echo(f"\n  Note saved: {path}")
        click.echo("  Remember to commit and push so it syncs to Obsidian.")
    elif choice == "2":
        notes = list_notes()
        click.echo(f"\n  {len(notes)} notes in vault (newest first):")
        for path in notes[:20]:
            click.echo(f"  - {path.relative_to(VAULT_DIR)}")
    elif choice == "3":
        query = input("  Search for: ").strip()
        matches = search_notes(query)
        click.echo(f"\n  {len(matches)} matching notes:")
        for path in matches[:20]:
            click.echo(f"  - {path.relative_to(VAULT_DIR)}")
    elif choice == "4":
        click.echo("\n" + recall())
    elif choice == "5":
        entry = input("  What should Claude remember? ").strip()
        if entry:
            remember(entry)
            click.echo(f"  Saved to {MEMORY_FILE}")
    else:
        click.echo("  Invalid choice.")


if __name__ == "__main__":
    def _save(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Saved: {path}")
        return True
    run(_save)
