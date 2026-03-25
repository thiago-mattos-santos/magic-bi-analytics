import gspread
import os
import psycopg2
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path


# Create and return authenticated gspread client.
def get_gspread_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    base_dir = Path(__file__).resolve().parent.parent
    json_path = base_dir / os.getenv("GSHEETS_SERVICE_ACCOUNT_JSON")

    creds = ServiceAccountCredentials.from_json_keyfile_name(str(json_path),
                                                             scope)
    return gspread.authorize(creds)


# Create and return PostgresSQL connection.
def db_connection():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT", "5432")),
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )

    return conn
