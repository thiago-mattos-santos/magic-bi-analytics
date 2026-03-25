import os
import connections as conn
from dotenv import load_dotenv

load_dotenv()


def update_versus_sheet(df_result):
    # Authentication
    client = conn.get_gspread_client()

    # Open versus
    spreadsheet_id = os.getenv("GSHEETS_SPREADSHEET_ID")
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(os.getenv("GSHEETS_TAB_VERSUS"))

    # Clean
    sheet.clear()

    # Upload data
    data = [df_result.columns.values.tolist()] + df_result.values.tolist()

    sheet.update(data)
