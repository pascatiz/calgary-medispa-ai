#!/usr/bin/env python3
"""
Calgary MediSpa AI - Google Workspace Placeholder

This file outlines where to add Google Workspace integration.
DO NOT hardcode credentials here. Use .env and service account files.

To activate Google Workspace integration:
1. Create a Google Cloud Project at console.cloud.google.com
2. Enable: Google Drive API, Google Sheets API, Gmail API
3. Create a Service Account and download the JSON key
4. Place the JSON key at config/service_account.json (NOT committed to git)
5. Set GOOGLE_SERVICE_ACCOUNT_FILE in your .env file
6. Share your Drive/Sheets with the service account email
"""

import os
from pathlib import Path


# ─────────────────────────────────────────────
# CONFIGURATION (loaded from .env)
# ─────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "config/service_account.json")
DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "")

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
]


def get_credentials():
    """
    PLACEHOLDER: Return Google API credentials from service account file.
    Requires: google-auth, google-auth-oauthlib, google-api-python-client
    Install: pip install google-auth google-auth-oauthlib google-api-python-client
    """
    # TODO: Implement after installing google packages
    # from google.oauth2 import service_account
    # creds = service_account.Credentials.from_service_account_file(
    #     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # return creds
    raise NotImplementedError("Google credentials not configured. See .env.example.")


def upload_to_drive(filepath, folder_id=None):
    """
    PLACEHOLDER: Upload a file to Google Drive.
    filepath: local path to file
    folder_id: Google Drive folder ID (from URL)
    """
    # TODO: Implement after configuring credentials
    # from googleapiclient.discovery import build
    # from googleapiclient.http import MediaFileUpload
    # service = build("drive", "v3", credentials=get_credentials())
    # file_metadata = {"name": Path(filepath).name}
    # if folder_id:
    #     file_metadata["parents"] = [folder_id]
    # media = MediaFileUpload(filepath, resumable=True)
    # result = service.files().create(body=file_metadata, media_body=media).execute()
    # return result.get("id")
    print(f"PLACEHOLDER: Would upload {filepath} to Google Drive folder {folder_id or DRIVE_FOLDER_ID}")
    return None


def append_to_sheet(sheet_id, range_name, values):
    """
    PLACEHOLDER: Append rows to a Google Sheet.
    sheet_id: Google Sheets document ID (from URL)
    range_name: e.g. "Sheet1!A1"
    values: list of lists, e.g. [["Name", "Hours", "Date"]]
    """
    # TODO: Implement after configuring credentials
    # from googleapiclient.discovery import build
    # service = build("sheets", "v4", credentials=get_credentials())
    # body = {"values": values}
    # service.spreadsheets().values().append(
    #     spreadsheetId=sheet_id, range=range_name,
    #     valueInputOption="RAW", body=body).execute()
    print(f"PLACEHOLDER: Would append {len(values)} rows to sheet {sheet_id} at {range_name}")


def create_calendar_event(calendar_id, title, start_time, end_time, description=""):
    """
    PLACEHOLDER: Create a Google Calendar event.
    start_time, end_time: ISO 8601 strings, e.g. "2024-01-15T10:00:00"
    """
    # TODO: Implement after configuring credentials
    # from googleapiclient.discovery import build
    # service = build("calendar", "v3", credentials=get_credentials())
    # event = {
    #     "summary": title,
    #     "description": description,
    #     "start": {"dateTime": start_time, "timeZone": "America/Edmonton"},
    #     "end": {"dateTime": end_time, "timeZone": "America/Edmonton"},
    # }
    # service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"PLACEHOLDER: Would create calendar event '{title}' from {start_time} to {end_time}")


def check_credentials_configured():
    """Check if Google credentials have been configured."""
    sa_file = Path(SERVICE_ACCOUNT_FILE)
    if not sa_file.exists():
        return False, f"Service account file not found: {SERVICE_ACCOUNT_FILE}"
    if not DRIVE_FOLDER_ID and not SHEETS_ID:
        return False, "No GOOGLE_DRIVE_FOLDER_ID or GOOGLE_SHEETS_ID set in .env"
    return True, "Google Workspace credentials appear configured"


def status():
    """Print configuration status for Google Workspace."""
    ok, msg = check_credentials_configured()
    print(f"Google Workspace: {'CONFIGURED' if ok else 'NOT CONFIGURED'} — {msg}")
    print(f"Service Account File: {SERVICE_ACCOUNT_FILE}")
    print(f"Drive Folder ID: {DRIVE_FOLDER_ID or '[not set]'}") 
    print(f"Sheets ID: {SHEETS_ID or '[not set]'}")
    print(f"Calendar ID: {CALENDAR_ID or '[not set]'}")


if __name__ == "__main__":
    status()
