import os
import connections
import logging
from psycopg2.extras import execute_values
from datetime import date

logger = logging.getLogger(__name__)


def load_dim_player(players: list[str]) -> None:
    """
    Full refresh load for bi_magic.dim_player:
    - TRUNCATE table
    - INSERT all player_name values
    """
    if not players:
        raise ValueError('Players list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "dim_player"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = [(p,) for p in players]
                execute_values(cur, f"INSERT INTO {schema}.{table} (player_name) VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s players into %s.%s", len(players), schema, table)

    finally:
        conn.close()


def load_dim_color(colors: list[tuple[str, int]]) -> None:
    """
    Full refresh load for bi_magic.dim_color:
    - TRUNCATE table
    - INSERT all colors
    """
    if not colors:
        raise ValueError('Colors list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "dim_color"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = colors
                execute_values(cur, f"INSERT INTO {schema}.{table} (color, color_group) VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s colors into %s.%s", len(colors), schema, table)

    finally:
        conn.close()


def load_dim_season(season: list[int]) -> None:
    """
    Full refresh load for bi_magic.dim_season:
    - TRUNCATE table
    - INSERT all season values
    """
    if not season:
        raise ValueError('Season list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "dim_season"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = [(p,) for p in season]
                execute_values(cur, f"INSERT INTO {schema}.{table} (season) VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s season into %s.%s", len(season), schema, table)

    finally:
        conn.close()


def load_dim_commander(commanders: list[tuple[str, str]]) -> None:
    """
    Full refresh load for bi_magic.dim_commander:
    - TRUNCATE table
    - INSERT all commanders
    """
    if not commanders:
        raise ValueError('Commanders list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "dim_commander"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = commanders
                execute_values(cur, f"INSERT INTO {schema}.{table} (commander, color) VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s commanders into %s.%s", len(commanders), schema, table)

    finally:
        conn.close()


def load_dim_score_rule(score_rule: list[tuple[str, str, int, str]]) -> None:
    """
    Full refresh load for bi_magic.dim_score_rule:
    - TRUNCATE table
    - INSERT all score_rules
    """
    if not score_rule:
        raise ValueError('Score_rule list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "dim_score_rule"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = score_rule
                execute_values(cur, f"INSERT INTO {schema}.{table} (score_code, description, points, category) "
                                    f"VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s score rules into %s.%s", len(score_rule), schema, table)

    finally:
        conn.close()


def load_fact_games(fact_games: list[tuple[int, int, str, str, str, int, bool, bool, int, str, date, str]]) -> None:
    """
    Full refresh load for bi_magic.fact_games:
    - TRUNCATE table
    - INSERT all fact_games
    """
    if not fact_games:
        raise ValueError('Fact Games list is empty. Nothing to load.')

    schema = os.getenv("PG_SCHEMA", "bi_magic")
    table = "fact_games"

    conn = connections.db_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                # Full refresh
                cur.execute(f"TRUNCATE TABLE {schema}.{table} CASCADE;")

                # Bulk insert
                rows = fact_games
                execute_values(cur, f"INSERT INTO {schema}.{table} (id, id_game, player_name, commander,"
                                    f"color, position, winner, combo, num_of_players, duration, date, deck_key) "
                                    f"VALUES %s;",
                               rows)

                cur.execute(f"SELECT COUNT(*) FROM {schema}.{table};")
                count = cur.fetchone()[0]
                logger.info("Postgres row count after insert in %s.%s: %s", schema, table, count)

        logger.info("Loaded %s games into %s.%s", len(fact_games), schema, table)

    finally:
        conn.close()
