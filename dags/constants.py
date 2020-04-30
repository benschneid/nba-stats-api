from collections import OrderedDict

player_cols = OrderedDict({'PERSON_ID': 0, 'DISPLAY_FIRST_LAST': 3, 'DOB': 6, 'COUNTRY': 8, 'HEIGHT': 10, 'WEIGHT': 11,
                           'SEASON_EXP': 12, 'FROM_YEAR': 22, 'TO_YEAR': 23, 'DRAFT_YEAR': 27, 'DRAFT_ROUND': 28,
                           'DRAFT_NUMBER': 29, 'SCHOOL': 7, 'POSITION': 14})

game_cols = OrderedDict({'GAME_ID': 4, 'SEASON': 0, 'GAME_DATE': 5, 'PLAYOFFS': -1})

team_box_cols = OrderedDict({'MIN': 8, 'FGM': 9, 'FGA': 10, 'FG_PCT': 11, 'FG3M': 12, 'FG3A': 13, 'FG3_PCT': 14,
                             'FTM': 15, 'FTA': 16, 'FT_PCT': 17, 'OREB': 18, 'DREB': 19, 'REB': 20, 'AST': 21,
                             'STL': 22, 'BLK': 23, 'TOV': 24, 'PF': 25, 'PTS': 26, 'PLUS_MINUS': 27, 'TEAM_ID': 1,
                             'GAME_ID': 4, 'HOME': 6, 'WIN': 7, 'OPPONENT_TEAM_ID': -1})

player_box_cols = OrderedDict({'MIN': 8, 'FGM': 9, 'FGA': 10, 'FG_PCT': 11, 'FG3M': 12, 'FG3A': 13, 'FG3_PCT': 14,
                               'FTM': 15, 'FTA': 16, 'FT_PCT': 17, 'OREB': 18, 'DREB': 19, 'REB': 20, 'AST': 21,
                               'STL': 22, 'BLK': 23, 'TOV': 24, 'PF': 25, 'PTS': 26, 'PLUS_MINUS': 27, 'GAME_ID': 0,
                               'TEAM_ID': 1, 'PLAYER_ID': 4, 'STARTED': 6})

player_season_totals = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
                        'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'SEASON_ID', 'TEAM_ID',
                        'PLAYER_ID', 'GAMES', 'GAMES_STARTED']

team_season_totals = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
                      'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'OPPT_FGM', 'OPPT_FGA',
                      'OPPT_FG_PCT', 'OPPT_FG3M', 'OPPT_FG3A', 'OPPT_FG3_PCT', 'OPPT_FTM', 'OPPT_FTA', 'OPPT_FT_PCT',
                      'OPPT_OREB', 'OPPT_DREB', 'OPPT_REB', 'OPPT_AST', 'OPPT_STL', 'OPPT_BLK', 'OPPT_TOV', 'OPPT_PF',
                      'OPPT_PTS', 'TEAM_ID', 'SEASON_ID', 'GAMES', 'WINS', 'LOSSES']

