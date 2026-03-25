import os
import connections
import logging

logger = logging.getLogger(__name__)


def get_worksheet(tab_env_var: str):
    # Authentication
    client = connections.get_gspread_client()

    # Open Sheet
    spreadsheet_id = os.getenv("GSHEETS_SPREADSHEET_ID")
    spreadsheet = client.open_by_key(spreadsheet_id)

    return spreadsheet.worksheet(os.getenv(tab_env_var))


def extract_fact_games_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_GAMES")

    # Get last row with data in Column A (1)
    last_line = len(ws.col_values(1))

    # Get last row with data in From Column A (1) to Column L
    interval = f"A2:L{last_line}"
    values = ws.get(interval)

    return values


def extract_players_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_SETTINGS")

    # Read players range
    values = ws.get(os.getenv("GSHEETS_RANGE_PLAYERS"))

    return values


def extract_colors_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_SETTINGS")

    # Read colors range
    values = ws.get(os.getenv("GSHEETS_RANGE_COLORS"))

    return values


def extract_seasons_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_SETTINGS")

    # Read seasons range
    values = ws.get(os.getenv("GSHEETS_RANGE_SEASONS"))

    return values


def extract_commanders_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_SETTINGS")

    # Read commanders range
    values = ws.get(os.getenv("GSHEETS_RANGE_COMMANDERS"))

    return values


def extract_score_rules_raw():
    # Get Tab
    ws = get_worksheet("GSHEETS_TAB_SCORE_RULE")

    # Read score rule range
    values = ws.get(os.getenv("GSHEETS_RANGE_SCORE_RULE"))

    return values
