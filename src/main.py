import os
from dotenv import load_dotenv
import extract
import transform
import load
import logging


def main():
    load_dotenv()

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("googleapiclient").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     PLAYER                      #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Players
    raw_players = extract.extract_players_raw()

    # Transform Players
    players = transform.dedupe_sorted(transform.clean_1col_values(raw_players))

    if players:
        logger.info("Players extracted: %s", len(players))
        logger.info("First player: %s", players[0])
        logger.info("Last player: %s", players[-1])

        # Load Players
        load.load_dim_player(players)
    else:
        logger.warning("No players found. Skipping load.")

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     COLOR                       #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Colors
    raw_colors = extract.extract_colors_raw()

    # Transform Colors
    colors = transform.transform_colors(raw_colors)

    if colors:
        logger.info("Colors extracted: %s", len(colors))
        logger.info("First color: %s", colors[0])
        logger.info("Last color: %s", colors[-1])

        # Load Colors
        load.load_dim_color(colors)
    else:
        logger.info("No colors found. Skipping load.")

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     SEASON                      #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Season
    raw_season = extract.extract_seasons_raw()

    # Transform Season
    season = transform.transform_season(raw_season)

    if season:
        logger.info("Season extracted: %s", len(season))
        logger.info("First season: %s", season[0])
        logger.info("Last season: %s", season[-1])

        # Load Season
        load.load_dim_season(season)
    else:
        logger.info("No season found. Skipping load.")

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     COMMANDER                   #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Commanders
    raw_commanders = extract.extract_commanders_raw()

    # Transform Commanders
    commanders = transform.transform_commander(raw_commanders)

    if commanders:
        logger.info("Commanders extracted: %s", len(commanders))
        logger.info("First commander: %s", commanders[0])
        logger.info("Last commander: %s", commanders[-1])

        # Load Commanders
        load.load_dim_commander(commanders)
    else:
        logger.info("No commanders found. Skipping load.")

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     SCORE RULE                  #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Score Rule
    raw_score_rule = extract.extract_score_rules_raw()

    # Transform Score Rule
    score_rule = transform.transform_score_rule(raw_score_rule)

    if score_rule:
        logger.info("Score Rule extracted: %s", len(score_rule))
        logger.info("First score rule: %s", score_rule[0])
        logger.info("Last score rule: %s", score_rule[-1])

        # Load Score Rule
        load.load_dim_score_rule(score_rule)
    else:
        logger.info("No score rule found. Skipping load.")

    # - - - - - - - - - - - - - - - - - - - - - - - - #
    #                     FACT GAMES                  #
    # - - - - - - - - - - - - - - - - - - - - - - - - #

    # Extract Fact Games
    raw_fact_games = extract.extract_fact_games_raw()

    # Transform Fact Games
    fact_games = transform.transform_fact_games(raw_fact_games)

    if fact_games:
        logger.info("Games extracted: %s", len(fact_games))
        logger.info("First game: %s", fact_games[0])
        logger.info("Last game: %s", fact_games[-1])

        # Load Fact Games
        load.load_fact_games(fact_games)
    else:
        logger.info("No games found. Skipping load.")


if __name__ == "__main__":
    main()
