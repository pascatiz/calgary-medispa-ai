#!/usr/bin/env python3
"""
Calgary MediSpa AI - Daily Planner
Creates a structured daily priority plan for clinic leadership.
"""

import click
from datetime import datetime
from pathlib import Path

TIME_BLOCKS = [
    "7:00 AM - 8:00 AM",
    "8:00 AM - 9:00 AM",
    "9:00 AM - 10:00 AM",
    "10:00 AM - 11:00 AM",
    "11:00 AM - 12:00 PM",
    "12:00 PM - 1:00 PM",
    "1:00 PM - 2:00 PM",
    "2:00 PM - 3:00 PM",
    "3:00 PM - 4:00 PM",
    "4:00 PM - 5:00 PM",
    "5:00 PM - 6:00 PM",
]


def collect_input(prompt, allow_empty=False):
    while True:
        val = input(f"  {prompt}: ").strip()
        if val or allow_empty:
            return val
        click.echo("  (required — please enter a value)")


def collect_list(prompt, count=3):
    items = []
    click.echo(f"  {prompt}")
    for i in range(1, count + 1):
        val = input(f"    {i}. ").strip()
        items.append(val if val else "[Not set]")
    return items


def generate_plan(data):
    date = data["date"]
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines_out = [
        f"# Daily Plan — {date}",
        f"**Clinic:** Calgary MediSpa",
        f"**Generated:** {generated_at}",
        f"**Prepared by:** {data.get('name', '[Name]')}",
        "", "---", "",
        "## Top 3 Priorities",
        "",
    ]
    for i, p in enumerate(data["priorities"], 1):
        lines_out.append(f"- [ ] **Priority {i}:** {p}")
    lines_out.extend(["", "---", "", "## Time Blocks", ""])
    for block, task in zip(TIME_BLOCKS, data.get("time_blocks", [])):
        lines_out.append(f"| {block} | {task} |")
    lines_out.extend(["", "---", "", "## Follow-Up Actions", ""])
    for item in data.get("followups", []):
        lines_out.append(f"- [ ] {item}")
    lines_out.extend(["", "---", "", "## Staff Accountability", ""])
    for item in data.get("staff", []):
        lines_out.append(f"- [ ] {item}")
    lines_out.extend([
        "", "---", "",
        "## End of Day Reflection",
        "",
        "**What went well?** ___",
        "",
        "**What needs attention tomorrow?** ___",
        "",
        "**Energy level (1-10):** ___",
        "",
        "*Calgary MediSpa AI Daily Planner*",
    ])
    return "\n".join(lines_out)


def run(safe_save):
    click.echo("\n  DAILY PRIORITY PLANNER")
    click.echo("  Build your daily plan for Calgary MediSpa operations.\n")
    date = input("  Date (YYYY-MM-DD) or Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    name = input("  Your name/role (e.g. Dr. Smith / Clinic Manager): ").strip() or "[Name]"
    priorities = collect_list("Enter your TOP 3 priorities for today:", 3)
    click.echo("\n  Time blocks (press Enter to skip any):")
    time_blocks = []
    for block in TIME_BLOCKS:
        task = input(f"    {block}: ").strip()
        time_blocks.append(task if task else "—")
    followups = collect_list("\n  Follow-up actions (3 items):", 3)
    staff = collect_list("\n  Staff accountability items (3 items):", 3)
    data = {"date": date, "name": name, "priorities": priorities,
            "time_blocks": time_blocks, "followups": followups, "staff": staff}
    plan = generate_plan(data)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = Path("outputs") / f"Daily_Plan_{date.replace('-', '')}_{date_str}.md"
    saved = safe_save(filepath, plan)
    if saved:
        click.echo(f"\n  Daily plan saved: {filepath}")


if __name__ == "__main__":
    def _save(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Saved: {path}")
        return True
    run(_save)
