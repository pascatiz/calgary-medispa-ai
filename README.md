# Calgary MediSpa AI — Cloud Automation Command Centre

[![GitHub Codespaces](https://img.shields.io/badge/Open%20in-Codespaces-blue?logo=github)](https://codespaces.new/pascatiz/calgary-medispa-ai)

> **Control your clinic from anywhere. Paste commands from ChatGPT mobile or Claude into GitHub Codespaces — no local machine required.**

---

## What This System Does

This repository is a cloud-based AI automation command centre for Calgary MediSpa. It runs entirely inside GitHub Codespaces and gives you:

- **SOAP Note Generation** — Paste raw treatment notes, get structured audit-ready SOAP notes saved as Markdown files
- **Payroll Validation** — Upload a CSV and get an instant payroll audit report flagging errors, overtime, duplicates, and missing data
- **Injector Training Tracker** — Track onboarding checklists for injector staff through all certification stages
- **Marketing Content Pipeline** — Generate a 7-day social media content calendar for all service lines
- **Personal Productivity Suite** — Daily planner, meeting notes, weekly goals, KPI tracker, and time-block scheduling
- **Google Workspace Placeholders** — Ready-to-build hooks for Drive, Sheets, and Gmail integration

---

## Quick Start: Open in GitHub Codespaces

### Step 1 — Open Codespaces

1. Go to: `https://github.com/pascatiz/calgary-medispa-ai`
2. Click the green **Code** button
3. Click the **Codespaces** tab
4. Click **Create codespace on main**
5. Wait 60–90 seconds for the environment to build

### Step 2 — Install Dependencies

Once the terminal opens inside Codespaces, run:

```bash
pip install -r requirements.txt
npm install
```

### Step 3 — Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your actual values (never commit this file)
nano .env
```

### Step 4 — Run Your First Command

```bash
python cli.py status
```

---

## All Available Commands

```bash
# Check system status
python cli.py status

# View recent logs
python cli.py logs

# Generate a SOAP note (will prompt for input)
python cli.py run soap

# Validate payroll CSV
python cli.py run payroll

# Check injector training status
python cli.py run training

# Generate marketing content calendar
python cli.py run marketing

# Run productivity tools
python cli.py run productivity
```

---

## Mobile Control Workflow (ChatGPT or Claude)

You do not need to be at a computer to run this system. Here is the exact workflow:

### Step 1 — Open ChatGPT or Claude on your phone

### Step 2 — Paste this prompt:

```
I need to generate a SOAP note for a MediSpa treatment. 
Ask me for the raw notes, then give me the exact command 
I should paste into my GitHub Codespaces terminal.
```

### Step 3 — Provide your treatment notes to the AI

### Step 4 — The AI will give you a command like:

```bash
python cli.py run soap
```

Then paste any content it generates into the Codespaces terminal when prompted.

### Step 5 — The output is saved automatically

All outputs save to `/outputs/` with timestamps. All actions log to `/logs/`.

---

## Folder Structure

```
calgary-medispa-ai/
├── README.md                          # This file
├── .devcontainer/
│   └── devcontainer.json             # Codespaces environment config
├── requirements.txt                   # Python dependencies
├── package.json                       # Node.js dependencies
├── cli.py                             # Main command-line interface
├── .env.example                       # Environment variable template
├── logs/                              # All execution logs
│   └── .gitkeep
├── outputs/                           # All generated files
│   └── .gitkeep
├── soap/
│   └── soap_generator.py             # SOAP note generation
├── payroll/
│   └── payroll_validator.py          # Payroll audit and validation
├── training/
│   └── injector_training_tracker.py  # Staff onboarding tracker
├── marketing/
│   └── content_pipeline.py           # Social media content calendar
├── productivity/
│   ├── daily_planner.py              # Daily priority planner
│   ├── meeting_notes.py              # Meeting notes organizer
│   └── goal_tracker.py               # Goals and KPI tracker
├── google/
│   └── google_workspace_placeholder.py  # Google integration hooks
└── config/
    └── settings.example.json         # Configuration template
    ```

    ---

    ## Module Details

    ### SOAP Note Generator (`soap/`)

    Turns raw treatment notes or transcripts into structured SOAP notes including:
    - Subjective / Objective / Assessment / Plan sections
    - Chaperone and consent fields
    - Encounter duration
    - Audit-readiness notation

    ### Payroll Validator (`payroll/`)

    Audits CSV payroll exports for:
    - Missing employee names
    - Excessive hours (>44 hrs/week Ontario standard)
    - Overtime risk flags
    - Duplicate rows
    - Missing pay periods
    - Vacation pay placeholders

    ### Injector Training Tracker (`training/`)

    Tracks 8-stage onboarding:
    1. Orientation
    2. Consent forms
    3. Product knowledge
    4. Injection anatomy
    5. Emergency protocol
    6. Shadowing
    7. Supervised treatment
    8. Final sign-off

    ### Marketing Content Pipeline (`marketing/`)

    Generates 7-day content calendar covering:
    - Botox, Fillers, Weight Loss, Skin Care
    - Clinic trust / physician-led positioning
    - Promotional posts
    - Each post includes: Caption, CTA, Platform, and Image Idea

    ### Productivity Suite (`productivity/`)

    Tools for clinic leadership:
    - **Daily Planner** — Top 3 priorities, time blocks, follow-ups
    - **Meeting Notes** — Structured notes with action items
    - **Goal Tracker** — Weekly goals, KPI placeholders, staff accountability

    ---

    ## Daily Operations Example

    ```bash
    # Morning routine — run this every morning
    python cli.py run productivity

    # After a treatment — generate SOAP note
    python cli.py run soap

    # Monday — check training status
    python cli.py run training

    # Friday — validate payroll before submission
    python cli.py run payroll

    # Monthly — generate content calendar
    python cli.py run marketing
    ```

    ---

    ## Security and Privacy Warnings

    > **IMPORTANT — Read before using with real patient data**

    1. **Do not upload real patient names, DOB, or health information** to this system unless you have configured proper privacy safeguards compliant with Alberta's Health Information Act (HIA) and PIPEDA.

    2. **Never commit your `.env` file** to GitHub. It is listed in `.gitignore`. Keep API keys local.

    3. **GitHub Codespaces storage is not PHIPA/HIA-certified** for regulated health data by default. Use only de-identified or synthetic data during development and testing.

    4. **Review all generated outputs** before using in clinical documentation. AI outputs are drafts only — always verify by a licensed provider.

    5. **Audit logs are stored in `/logs/`** — review them regularly.

    ---

    ## Adding New Modules

    1. Create a new folder: `mkdir mymodule`
    2. Create your Python file: `mymodule/my_feature.py`
    3. Add a `run()` function that accepts optional arguments
    4. Register the command in `cli.py` under the `run` command dispatcher
    5. Update `README.md`

    ---

    ## Troubleshooting

    | Problem | Solution |
    |---|---|
    | `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
    | `Permission denied on /outputs` | Run `chmod 755 outputs/ logs/` |
    | Codespace won't start | Delete and recreate from the Codespaces tab |
    | CSV not found | Use the full path or run from repo root |
    | Output file already exists | CLI will ask you to confirm overwrite |

    ---

    ## Tech Stack

    - **Runtime**: Python 3.11 + Node.js 18
    - **Environment**: GitHub Codespaces (Ubuntu)
    - **Interface**: CLI via `cli.py`
    - **Storage**: Local `/outputs` and `/logs` directories
    - **Future**: Google Workspace API, OpenAI API, Twilio

    ---

    *Built for Calgary MediSpa operations. Not for general distribution.*
