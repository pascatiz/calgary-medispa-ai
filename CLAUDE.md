# Calgary MediSpa AI — Claude Code Instructions

This repository is the cloud automation command centre for Calgary MediSpa
(SOAP notes, payroll validation, injector training, marketing, productivity),
plus a git-synced Obsidian vault in `vault/`.

## Persistent memory — read this first

At the start of every session, read `vault/90-Claude-Memory/Memory.md`.
It is your long-term memory: owner preferences, clinic facts, and a log of
past sessions. Apply what it says.

As you work, keep the memory current so you improve over time:

- When the owner states a preference or corrects you, append it under
  `## Preferences` (dated bullet).
- When you learn a durable fact about the clinic or this system, append it
  under `## Clinic Facts`.
- At the end of a session where you changed something meaningful, add one
  line under `## Session Log`.
- Append entries either by editing the file directly or via
  `python cli.py remember "..." --section Preferences`.
- Keep entries short. Never store patient names, dates of birth, or health
  information in memory or in the vault (Alberta HIA / PIPEDA).

## Obsidian vault (`vault/`)

The `vault/` folder is the owner's Obsidian vault, synced through this git
repo. When the owner sends you a note, thought, or something to file away,
save it as a markdown note in the vault:

- Quick capture goes to `vault/00-Inbox/`.
- Use `python cli.py note "content" --title X --tags a,b` or write the file
  directly with YAML frontmatter (`created`, `source`, `tags`).
- Organized/long-lived notes go to `vault/10-Notes/`; clinic SOPs, meeting
  notes, and plans go to `vault/20-Clinic-Operations/`.
- Search existing notes with `python cli.py search "keyword"` before creating
  duplicates.

Vault and memory changes only reach the owner's Obsidian app after they are
committed and pushed. Always commit and push vault/memory updates before
ending a session (on the branch you were told to use).

## Conventions

- Python modules live in feature folders (`soap/`, `payroll/`, `obsidian/`, …)
  and expose a `run(safe_save)` entry point registered in `cli.py`.
- Generated outputs go to `outputs/`; actions are logged to `logs/cli.log`
  via `log_action()`.
- Never commit `.env`, credentials, CSVs, or patient data (see `.gitignore`).
