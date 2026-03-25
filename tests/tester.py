from dotenv import load_dotenv
from src import extract, transform
from datetime import datetime
import logging
import os
import re

level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, level, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.WARNING)
logging.getLogger("googleapiclient").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()

values = extract.extract_fact_games_raw()
result = []
pattern = r'^\d+:\d{2}:\d{2}$'
skipped_rows = 0


for row in values:
    if row and len(row) > 11 and row[0]:
        if str(row[2]).strip().lower() == 'null':
            continue

        row_id = int(row[0])
        id_game = int(row[1])
        player = str(row[2]).strip()
        commander = str(row[3]).strip()
        color = str(row[4]).strip()
        if ' - ' in color:
            _, color = color.split(" - ")
        else:
            logger.warning('Invalid color format. Skipping row_id: %s', row_id)
            skipped_rows += 1
            continue
        position = int(row[5])
        winner = transform.to_bool(row[6])
        combo = transform.to_bool(row[11])
        num_of_players = int(row[10])
        duration = str(row[7]).strip()
        if re.match(r'^\d+:\d{2}:\d{2}$', duration):
            pass
        else:
            logger.warning('Invalid duration format. Skipping row_id: %s', row_id)
            skipped_rows += 1
            continue
        game_date = datetime.strptime(row[8], '%m/%d/%Y').date()
        deck_key = str(row[9]).strip()

        result.append((row_id, id_game, player, commander, color, position, winner, combo,
                       num_of_players, duration, game_date, deck_key))

logger.info("Rows processed: %s", len(result))
logger.info("Rows skipped: %s", skipped_rows)

print(values[0])
print(result[0])
print("Rows processed: %s", len(result))
print("Rows skipped: %s", skipped_rows)
