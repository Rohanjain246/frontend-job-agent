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
        # Retrieve credentials and sheet ID from environment variables
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))

        # Authenticate using the service account
        creds = Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        client = gspread.authorize(creds)

        # Open the spreadsheet and select the first worksheet
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.sheet1

        # Convert DataFrame rows to a list of lists
        rows = []
        for _, row in df.iterrows():
            rows.append([
                str(row.get("company", "")),
                str(row.get("title", "")),
                str(row.get("score", "")),
                str(row.get("source", ""))
            ])

        # Append rows to the sheet if data exists
        if rows:
            worksheet.append_rows(rows)

        print("Google Sheet updated successfully.")

    except Exception as e:
        print("Google Sheets Error:", str(e))   
