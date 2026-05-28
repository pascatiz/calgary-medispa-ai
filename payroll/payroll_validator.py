#!/usr/bin/env python3
"""
Calgary MediSpa AI - Payroll Validator
Audits payroll CSV files for errors, overtime risk,
missing data, and compliance issues.
"""

import click
import csv
import os
from datetime import datetime
from pathlib import Path

MAX_WEEKLY_HOURS = float(os.getenv("PAYROLL_MAX_WEEKLY_HOURS", 44))
OVERTIME_THRESHOLD = float(os.getenv("PAYROLL_OVERTIME_THRESHOLD", 44))
VACATION_PAY_RATE = float(os.getenv("PAYROLL_VACATION_PAY_RATE", 0.04))

REQUIRED_COLUMNS = ["employee_name", "hours", "pay_period", "hourly_rate"]


def load_csv(filepath):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def check_columns(rows):
    issues = []
    if not rows:
        return ["CSV file is empty."]
    headers = [h.strip().lower() for h in rows[0].keys()]
    for col in REQUIRED_COLUMNS:
        if col not in headers:
            issues.append(f"MISSING COLUMN: '{col}' is required but not found")
    return issues


def check_missing_names(rows):
    issues = []
    for i, row in enumerate(rows, start=2):
        name_key = next((k for k in row.keys() if k.strip().lower() == "employee_name"), None)
        if name_key and not row[name_key].strip():
            issues.append(f"ROW {i}: Missing employee name")
    return issues


def check_hours(rows):
    issues = []
    for i, row in enumerate(rows, start=2):
        hours_key = next((k for k in row.keys() if k.strip().lower() == "hours"), None)
        if hours_key:
            try:
                hours = float(row[hours_key])
                name = row.get("employee_name", "Unknown")
                if hours > MAX_WEEKLY_HOURS:
                    issues.append(f"ROW {i}: OVERTIME RISK -- {name} has {hours} hrs (max {MAX_WEEKLY_HOURS})")
                if hours <= 0:
                    issues.append(f"ROW {i}: ZERO/NEGATIVE hours for {name}")
                if hours > 80:
                    issues.append(f"ROW {i}: SUSPICIOUS -- {name} has {hours} hrs (>80, likely data error)")
            except (ValueError, TypeError):
                issues.append(f"ROW {i}: INVALID hours value: '{row.get(hours_key, '')}'")
    return issues


def check_duplicates(rows):
    issues = []
    seen = {}
    for i, row in enumerate(rows, start=2):
        name = row.get("employee_name", "").strip().lower()
        period = row.get("pay_period", "").strip().lower()
        key = f"{name}|{period}"
        if key in seen:
            issues.append(f"ROW {i}: DUPLICATE -- {row.get('employee_name', 'Unknown')} for period '{period}' (also at row {seen[key]})")
        else:
            seen[key] = i
    return issues


def check_pay_period(rows):
    issues = []
    for i, row in enumerate(rows, start=2):
        period_key = next((k for k in row.keys() if k.strip().lower() == "pay_period"), None)
        if period_key and not row[period_key].strip():
            issues.append(f"ROW {i}: Missing pay period for {row.get('employee_name', 'Unknown')}")
    return issues


def calculate_vacation_pay(rows):
    summaries = []
    for row in rows:
        try:
            hours = float(row.get("hours", 0))
            rate = float(row.get("hourly_rate", 0))
            gross = hours * rate
            vac_pay = gross * VACATION_PAY_RATE
            summaries.append({
                "name": row.get("employee_name", "Unknown"),
                "hours": hours, "rate": rate,
                "gross": gross, "vacation_pay": vac_pay,
                "total": gross + vac_pay,
            })
        except (ValueError, TypeError):
            continue
    return summaries


def generate_report(filepath, all_issues, summaries, rows):
    total_issues = sum(len(v) for v in all_issues.values())
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Payroll Audit Report",
        f"**Clinic:** Calgary MediSpa",
        f"**Generated:** {generated_at}",
        f"**Source File:** {filepath}",
        f"**Total Employees:** {len(rows)}",
        f"**Total Issues Found:** {total_issues}",
        "", "---", "",
    ]
    status = "PASS" if total_issues == 0 else "REVIEW REQUIRED"
    lines.append(f"## Status: {status}")
    if total_issues == 0:
        lines.append("No issues found. Payroll data appears clean.")
    else:
        lines.append(f"{total_issues} issue(s) require attention before payroll submission.")
    lines.extend(["", "---", ""])
    for category, issues in all_issues.items():
        lines.append(f"## {category}")
        if not issues:
            lines.append("- No issues found")
        else:
            for issue in issues:
                lines.append(f"- {issue}")
        lines.append("")
    lines.extend(["---", "", "## Vacation Pay Estimates"])
    lines.append(f"*Rate: {VACATION_PAY_RATE*100:.0f}%*")
    lines.append("")
    lines.append("| Employee | Hours | Rate | Gross | Vac Pay | Total |")
    lines.append("|---|---|---|---|---|---|")
    for s in summaries:
        lines.append(f"| {s['name']} | {s['hours']} | ${s['rate']:.2f} | ${s['gross']:.2f} | ${s['vacation_pay']:.2f} | ${s['total']:.2f} |")
    lines.extend(["", "---", "",
        "## Notes",
        "- This is a preliminary audit tool only",
        "- Verify with your payroll provider before submitting",
        "- Overtime threshold: 44 hrs/week (Alberta Employment Standards)",
        "- Retain payroll records for minimum 3 years",
        "", "*Generated by Calgary MediSpa AI*"])
    return "\n".join(lines)


def run(safe_save):
    click.echo("\n  PAYROLL VALIDATOR")
    click.echo("  Validates payroll CSV data.\n")
    csv_path = input("  Enter path to payroll CSV file: ").strip()
    if not csv_path:
        click.echo("  ERROR: No file path provided.")
        return
    csv_path = Path(csv_path)
    if not csv_path.exists():
        click.echo(f"  ERROR: File not found: {csv_path}")
        return
    click.echo(f"  Loading: {csv_path}...")
    try:
        rows = load_csv(str(csv_path))
    except Exception as e:
        click.echo(f"  ERROR loading CSV: {e}")
        return
    click.echo(f"  Loaded {len(rows)} records. Running checks...")
    all_issues = {
        "Column Structure": check_columns(rows),
        "Missing Employee Names": check_missing_names(rows),
        "Hours Validation": check_hours(rows),
        "Duplicate Entries": check_duplicates(rows),
        "Pay Period": check_pay_period(rows),
    }
    summaries = calculate_vacation_pay(rows)
    report = generate_report(str(csv_path), all_issues, summaries, rows)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Payroll_Audit_{date_str}.md"
    filepath = Path("outputs") / filename
    total_issues = sum(len(v) for v in all_issues.values())
    click.echo(f"\n  Audit complete. {total_issues} issue(s) found.")
    saved = safe_save(filepath, report)
    if saved:
        click.echo(f"\n  Report saved: {filepath}")


if __name__ == "__main__":
    def _save(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"Saved: {path}")
        return True
    run(_save)
