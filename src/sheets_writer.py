import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive"
]

def update_sheet(df):


try:
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    service_account_info = json.loads(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    )

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)

    worksheet = sheet.sheet1

    rows = []

    for _, row in df.iterrows():
        rows.append([
            str(row.get("company", "")),
            str(row.get("title", "")),
            str(row.get("score", "")),
            str(row.get("source", ""))
        ])

    if rows:
        worksheet.append_rows(rows)

    print("Google Sheet updated")

except Exception as e:
    print("Google Sheets Error:", str(e))
