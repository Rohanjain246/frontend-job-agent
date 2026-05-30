import json
import os
from datetime import date

import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_ID             = os.getenv("GOOGLE_SHEET_ID", "")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")

# Exact column order the user asked for
COLUMNS = [
    "Date", "Company", "Role", "Score", "Source",
    "URL", "Applied", "ApplicationDate", "Interview Status", "Offer", "Notes",
]


def _get_client():
    creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
    creds      = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def _ensure_sheet(spreadsheet, tab_name: str):
    """Return worksheet, creating it with headers if it doesn't exist."""
    try:
        ws = spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=tab_name, rows=1000, cols=len(COLUMNS))

    # Write header if sheet is empty or header is wrong
    existing = ws.row_values(1)
    if existing != COLUMNS:
        ws.clear()
        ws.append_row(COLUMNS, value_input_option="USER_ENTERED")

    return ws


def _existing_keys(ws) -> set:
    """Return set of 'company|role' for all rows already in the sheet."""
    rows = ws.get_all_values()[1:]   # skip header
    return {
        f"{r[1].strip().lower()}|{r[2].strip().lower()}"
        for r in rows
        if len(r) >= 3
    }


def _build_row(job: dict, today: str) -> list:
    url = str(job.get("url", "") or "")

    # Clickable hyperlink formula — shows "Apply →" as the label
    if url.startswith("http"):
        link_cell = f'=HYPERLINK("{url}","Apply →")'
    else:
        link_cell = url

    return [
        today,
        str(job.get("company", "")),
        str(job.get("title",   "")),
        int(job.get("score",   0)),
        str(job.get("source",  "")),
        link_cell,
        "",   # Applied          — user fills in
        "",   # ApplicationDate  — user fills in
        "",   # Interview Status — user fills in
        "",   # Offer            — user fills in
        "",   # Notes            — user fills in
    ]


def push_to_sheet(df):
    """
    Push all jobs to 'All Jobs' tab and 80+ ATS jobs to 'Strong Matches (80+)' tab.
    Skips rows that already exist (deduplication by Company + Role).
    Clickable 'Apply →' links in the URL column.
    """
    if not SHEET_ID or not SERVICE_ACCOUNT_JSON:
        print("Sheets: skipping — GOOGLE_SHEET_ID or GOOGLE_SERVICE_ACCOUNT_JSON not set")
        print("  → See .env.example for setup instructions")
        return

    try:
        client      = _get_client()
        spreadsheet = client.open_by_key(SHEET_ID)
        today       = date.today().isoformat()

        # ── Tab 1: All Jobs ──────────────────────────────────────────────────
        ws_all    = _ensure_sheet(spreadsheet, "All Jobs")
        seen_all  = _existing_keys(ws_all)
        new_all   = []

        for _, job in df.iterrows():
            key = f"{str(job.get('company','')).strip().lower()}|{str(job.get('title','')).strip().lower()}"
            if key in seen_all:
                continue
            seen_all.add(key)
            new_all.append(_build_row(job.to_dict(), today))

        if new_all:
            ws_all.append_rows(new_all, value_input_option="USER_ENTERED")
            print(f"Sheets ✓  'All Jobs' — added {len(new_all)} new rows")
        else:
            print("Sheets ✓  'All Jobs' — nothing new to add")

        # ── Tab 2: Strong Matches (80+) ──────────────────────────────────────
        df_strong  = df[df["score"] >= 80].copy()
        ws_strong  = _ensure_sheet(spreadsheet, "Strong Matches (80+)")
        seen_str   = _existing_keys(ws_strong)
        new_strong = []

        for _, job in df_strong.iterrows():
            key = f"{str(job.get('company','')).strip().lower()}|{str(job.get('title','')).strip().lower()}"
            if key in seen_str:
                continue
            seen_str.add(key)
            new_strong.append(_build_row(job.to_dict(), today))

        if new_strong:
            ws_strong.append_rows(new_strong, value_input_option="USER_ENTERED")
            print(f"Sheets ✓  'Strong Matches (80+)' — added {len(new_strong)} rows")
        else:
            print(f"Sheets ✓  'Strong Matches (80+)' — {len(df_strong)} matches found, none new")

    except json.JSONDecodeError:
        print("Sheets error: GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON")
    except gspread.SpreadsheetNotFound:
        print("Sheets error: sheet not found — check GOOGLE_SHEET_ID and sharing permissions")
    except Exception as e:
        print(f"Sheets error: {e}")
