import numpy as np
import pandas as pd
from src.analytics.upload_data_sheet import get_sheet_data
from src.analytics.upload_data_sheet import update_versus_sheet

# Puxar dados da planilha
raw_data = get_sheet_data()

# Transformar em DataFrame
df = pd.DataFrame(raw_data[1:], columns=raw_data[0])

# Ajustar Booleanos de String para Boolean
df['winner'] = df['winner'].map({'TRUE': True, 'FALSE': False})
df['combo'] = df['combo'].map({'TRUE': True, 'FALSE': False})

# Remover jogadores 'null' e criar df_all_games
df_all_games = (
    df.loc[df['player'] != 'null', ['id_game', 'player', 'winner']]
    .copy()
)
df_all_games['winner'] = df_all_games['winner'].astype(bool)

# Winners and Losers
df_winners = df_all_games[df_all_games['winner']]  # Pandas filters TRUE automatically
df_losers = df_all_games[~df_all_games['winner']]  # ~ means opposition


# The code below is a translation of this SQL Query
'''
SELECT  a.players AS winner,
        b.players AS loser,
        COUNT(b.players) AS victories

FROM a.df_winners
LEFT JOIN b.df_losers ON a.id_game = b.id_game

GROUP BY a.players, b.players
ORDER BY 1, 3, 2
'''
# Left Join
df_result = (
    pd.merge(df_winners,
             df_losers,
             on='id_game',
             how='left',
             suffixes=('_win', '_lose'))
    .groupby(['player_win', 'player_lose'])
    .size()
    .reset_index(name='victories')
    .sort_values(by=['player_win', 'victories', 'player_lose'], ascending=[True, False, True])
    .reset_index(drop=True)
)

# Função que gera todos os pares (main_player, adversário) por partida


# -------------------------------
# Gerar todos os pares (vetorizado, sem loops)
# -------------------------------
df_pairs = df_all_games.merge(df_all_games, on='id_game')  #itself join
df_pairs = df_pairs[df_pairs['player_x'] != df_pairs['player_y']]  # remover par consigo mesmo
df_pairs = df_pairs.rename(columns={'player_x': 'main_player', 'player_y': 'opponent'})

df_matches = df_pairs.groupby(['main_player', 'opponent']).size().reset_index(name='matches')

df_result = (
    pd.merge(df_result,
             df_matches,
             left_on=['player_win', 'player_lose'],
             right_on=['main_player', 'opponent'],
             how='left')

)

# Se houver NaN, substituir por 0 antes de converter
df_result['matches'] = df_result['matches'].fillna(0).astype(int)
df_result['win_rate'] = df_result['victories'] / df_result['matches']
df_result['win_rate'] = df_result['win_rate'].fillna(0)
df_result['win_rate'] = df_result['win_rate'].round(3)
df_result = df_result[['player_win', 'player_lose', 'victories', 'matches', 'win_rate']]
df_result = df_result.sort_values(by=['player_win', 'win_rate', 'victories'], ascending=[True, False, False])

# Substituir infinitos por 0
df_result['win_rate'].replace([np.inf, -np.inf], 0, inplace=True)

# Substituir NaN por 0
df_result['win_rate'].fillna(0, inplace=True)


update_versus_sheet(df_result)
