from datetime import datetime, date
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


# Clean empty values such as [], [''], [' '] and trim
def clean_1col_values(values: list[list]) -> list[str]:
    cleaned = [
        str(row[0]).strip()
        for row in values
        if row and len(row) > 0 and row[0] is not None and str(row[0]).strip()
    ]
    return cleaned


# Remove duplicates and sort
def dedupe_sorted(items: list[str]) -> list[str]:
    return sorted(set(items))


# convert yes/no, str(True/False, 1/0 to boolean
def to_bool(value) -> bool:
    if value is None:
        return False
    v = str(value).strip().lower()
    return v in {'true', '1', 'yes', 'y', 'sim'}


def transform_colors(values: list[list]) -> list[tuple[str, int]]:
    result = []

    for row in values:
        if row and row[0] and str(row[0]).strip():
            value = str(row[0]).strip()

            group_str, color = value.split(" - ")
            group = int(group_str)

            result.append((color, group))

    return result


def transform_season(values: list[list]) -> list[int]:
    result = []

    for row in values:
        if row and row[0] and str(row[0]).strip():
            value = str(row[0]).strip()

            if value == "ALL":
                continue

            result.append(int(value))

    return result


def transform_commander(values: list[list]) -> list[tuple[str, str]]:
    result = []

    for row in values:
        if row and len(row) > 2 and row[0] and row[2]:
            commander = str(row[0]).strip()

            value = str(row[2]).strip()
            _, color = value.split(" - ")

            result.append((commander, color))

    return result


def transform_score_rule(values: list[list]) -> list[tuple[str, str, int, str]]:
    bonus = {'TCM', 'TCV', 'TCW', 'TPM', 'TPV', 'TPW'}
    result = []

    for row in values:
        if row and len(row) > 2 and row[0] and row[1] and row[2]:
            code = str(row[0]).strip()
            description = str(row[1]).strip()
            points = int(row[2])

            if code in bonus:
                result.append((code, description, points, 'Bonus'))
            else:
                result.append((code, description, points, 'General'))

    return result


def transform_fact_games(
        values: list[list]
) -> list[tuple[int, int, str, str, str, int, bool, bool, int, str, date, str]]:
    result = []
    pattern = r'^\d+:\d{2}:\d{2}$'
    skipped_rows = 0

    for row in values:
        if row and len(row) > 11 and row[0]:

            # Null players must be ignored
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
            winner = to_bool(row[6])
            combo = to_bool(row[11])
            num_of_players = int(row[10])

            duration = str(row[7]).strip()
            if not re.match(pattern, duration):
                logger.warning('Invalid duration format. Skipping row_id: %s', row_id)
                skipped_rows += 1
                continue

            game_date = datetime.strptime(row[8], '%m/%d/%Y').date()
            deck_key = str(row[9]).strip()

            result.append((row_id, id_game, player, commander, color, position, winner, combo,
                           num_of_players, duration, game_date, deck_key))

    logger.info("Fact Games - Valid rows processed: %s", len(result))
    logger.info("Fact Games - Rows skipped: %s", skipped_rows)

    if skipped_rows > 0:
        logger.warning("Fact Games - Skipped rows during processing: %s", skipped_rows)

    return result
