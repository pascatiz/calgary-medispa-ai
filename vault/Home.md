---
created: 2026-07-08
tags:
  - dashboard
---

# Calgary MediSpa Vault

Welcome. This vault is git-synced with the [calgary-medispa-ai](https://github.com/pascatiz/calgary-medispa-ai) repository. Notes added from Claude Code appear here after a push; notes you write in Obsidian sync back with the Obsidian Git plugin.

## Folders

- [[00-Inbox]] — quick capture from Claude Code and mobile. Triage regularly.
- [[10-Notes]] — organized notes after triage.
- [[20-Clinic-Operations]] — SOPs, meeting notes, training, marketing plans.
- [[90-Claude-Memory]] — Claude's persistent memory. It reads this every session and learns over time.

## Capturing notes from Claude Code

Tell Claude what to note, or run directly:

```bash
python cli.py note "Called supplier about filler restock" --tags ops,inventory
python cli.py remember "Prefers SOAP notes in bullet form"
python cli.py recall
```
