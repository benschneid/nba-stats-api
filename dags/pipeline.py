from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow import AirflowException
from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_
from nba_api.stats.endpoints import leaguegamelog, boxscoretraditionalv2, commonplayerinfo
from datetime import datetime
from models import Base, BaseProd, LeagueGameLog, Player, PlayerBoxStage, TeamSeasonReg as tsr, TeamSeasonPost as tsp,\
    PlayerSeasonReg as psr, PlayerSeasonPost as psp, CleanTeamBoxStage, CleanPlayerBoxStage
import time
from collections import OrderedDict

default_args = {
    "owner": "airflow",
    "start_date": datetime(1969, 10, 1),
    "end_date": datetime(2017, 6, 30),
    "retries": 0,
}

dag = DAG("nba_api_to_postgres", default_args=default_args, schedule_interval='0 0 * 10,11,12,1,2,3,4,5,6 *',
          max_active_runs=15)


def get_engine(conn_id):
    connection = BaseHook.get_connection(conn_id)
    connection_uri = '{c.conn_type}+psycopg2://{c.login}:{c.password}@{c.host}:{c.port}/{c.schema}'.format(c=connection)
    return create_engine(connection_uri)


engine = get_engine('postgres_bbref')
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()


def initialize_db():
    engine.execute('CREATE SCHEMA IF NOT EXISTS stage;')
    engine.execute('CREATE SCHEMA IF NOT EXISTS prod;')
    Base.metadata.create_all(engine)
    BaseProd.metadata.create_all(engine)


def games_request(season_string, bb_date, season_type):
    return leaguegamelog.LeagueGameLog(season=season_string, date_from_nullable=bb_date,
                                       date_to_nullable=bb_date,
                                       season_type_all_star=season_type).get_dict()['resultSets'][0]['rowSet']


def stage_game_logs(**kwargs):
    date = kwargs['ds']
    split_date = date.split('-')
    bb_date = split_date[1]+'/'+split_date[2]+'/'+split_date[0]
    if int(split_date[1]) > 7:
        season_year = int(split_date[0])
    else:
        season_year = int(split_date[0]) - 1
    season_string = str(season_year) + '-' + str(season_year+1)[-2:]
    poss_post = int(split_date[1]) in range(3, 7)
    stats = games_request(season_string, bb_date, "Playoffs" if poss_post else "Regular Season")
    if stats:
        insert_content = str(stats)[1:-1].replace("[", "(").replace("]", ", True)" if poss_post else ", False)").replace("None", "Null")
        conn.execute("INSERT INTO stage.league_game_log VALUES " + insert_content + " ON CONFLICT DO NOTHING")
    else:
        time.sleep(3)
        stats = games_request(season_string, bb_date, "Regular Season" if poss_post else "Playoffs")
        if stats:
            insert_content = str(stats)[1:-1].replace("[", "(").replace("]", ", False)" if poss_post else ", True)").replace("None", "Null")
            conn.execute("INSERT INTO stage.league_game_log VALUES " + insert_content + " ON CONFLICT DO NOTHING")
        else:
            raise AirflowException('No game data for this date')


def stage_player_boxes(**kwargs):
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    for game in game_ids_tuple:
        stats = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game).get_dict()['resultSets'][0]['rowSet']
        time.sleep(3)
        for m, stat in enumerate(stats):
            for n, item in enumerate(stat):
                if type(item) == str:
                    if "'" in item:
                        stats[m][n] = item.replace("'", "''")
        insert_content = str(stats)[1:-1].replace("[", "(").replace("]", ")").replace("None", "Null").replace('"', "'")
        conn.execute("INSERT INTO stage.player_box VALUES " + insert_content + " ON CONFLICT DO NOTHING")


player_cols = OrderedDict({'PERSON_ID': 0, 'DISPLAY_FIRST_LAST': 3, 'DOB': 6, 'COUNTRY': 8, 'HEIGHT': 10, 'WEIGHT': 11,
                           'SEASON_EXP': 12, 'FROM_YEAR': 22, 'TO_YEAR': 23, 'DRAFT_YEAR': 27, 'DRAFT_ROUND': 28,
                           'DRAFT_NUMBER': 29, 'SCHOOL': 7, 'POSITION': 14})


def insert_new_players(**kwargs):
    date_format_str = '%Y-%m-%d'
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    staged_player_box_tuple = session.query(PlayerBoxStage.PLAYER_ID).filter(PlayerBoxStage.GAME_ID.in_(game_ids_tuple)).all()
    staged_players = [player[0] for player in staged_player_box_tuple]
    for player in staged_players:
        if not session.query(Player.PLAYER_ID).filter(Player.PLAYER_ID == player).first():
            new_player = commonplayerinfo.CommonPlayerInfo(player_id=player).get_dict()['resultSets'][0]['rowSet'][0]
            for n, col in enumerate(new_player):
                if col in ['', ' ']:
                    new_player[n] = None
            new_player[player_cols['DOB']] = datetime.strptime(new_player[player_cols['DOB']][0:10],
                                                               date_format_str).strftime('%Y-%m-%d %H:%M:%S')
            if new_player[player_cols['HEIGHT']]:
                height_split = [int(i) for i in new_player[player_cols['HEIGHT']].split('-')]
                new_player[player_cols['HEIGHT']] = height_split[0]*12 + height_split[1]
            for col in ['WEIGHT', 'DRAFT_YEAR', 'DRAFT_ROUND', 'DRAFT_NUMBER']:
                if new_player[player_cols[col]] and new_player[player_cols[col]] != 'Undrafted':
                    new_player[player_cols[col]] = int(new_player[player_cols[col]])
                else:
                    new_player[player_cols[col]] = None
            limited_content = [new_player[value] for key, value in player_cols.items()]
            for n, item in enumerate(limited_content):
                if type(item) == str:
                    if "'" in item:
                        limited_content[n] = item.replace("'", "''")
            insert_content = str(limited_content).replace("[", "(").replace("]", ")").replace("None", "Null").replace('"',"'")
            conn.execute("INSERT INTO prod.players VALUES " + insert_content + " ON CONFLICT DO NOTHING")
            time.sleep(4)


game_cols = OrderedDict({'GAME_ID': 4, 'SEASON': 0, 'GAME_DATE': 5, 'PLAYOFFS': -1})


def insert_games(**kwargs):
    date = kwargs['ds']
    date_format_str = '%Y-%m-%d'
    league_game_logs = session.query(LeagueGameLog.__table__).filter(LeagueGameLog.GAME_DATE == date).all()
    if league_game_logs:
        for n, i in enumerate(league_game_logs):
            league_game_logs[n] = list(i)
        for i in league_game_logs:
            year = int(i[0][1:])
            i[0] = str(year) + '-' + str(year + 1)[-2:]
            i[5] = datetime.strptime(i[5], date_format_str).strftime('%Y-%m-%d %H:%M:%S')

        games = [[league_game_logs[n][value] for key, value in game_cols.items()] for n, i in enumerate(league_game_logs)]
        insert_content = str(games[0::2])[1:-1].replace("[", "(").replace("]", ")").replace("None", "Null").replace('"', "'")
        conn.execute("INSERT INTO prod.games VALUES " + insert_content + " ON CONFLICT DO NOTHING")


team_box_cols = OrderedDict({'MIN': 8, 'FGM': 9, 'FGA': 10, 'FG_PCT': 11, 'FG3M': 12, 'FG3A': 13, 'FG3_PCT': 14,
                             'FTM': 15, 'FTA': 16, 'FT_PCT': 17, 'OREB': 18, 'DREB': 19, 'REB': 20, 'AST': 21,
                             'STL': 22, 'BLK': 23, 'TOV': 24, 'PF': 25, 'PTS': 26, 'PLUS_MINUS': 27, 'TEAM_ID': 1,
                             'GAME_ID': 4, 'HOME': 6, 'WIN': 7, 'OPPONENT_TEAM_ID': -1})


def insert_team_box(**kwargs):
    date = kwargs['ds']
    league_game_logs = session.query(LeagueGameLog.__table__).filter(LeagueGameLog.GAME_DATE == date).all()
    if league_game_logs:
        for n, i in enumerate(league_game_logs):
            league_game_logs[n] = list(i)
            if n % 2 == 0:
                league_game_logs[n].append(league_game_logs[n+1][1])
            else:
                league_game_logs[n].append(league_game_logs[n-1][1])
        for i in league_game_logs:
            i[6] = False if '@' in i[6] else True
            i[7] = True if i[7] == 'W' else False
        team_boxes = [[league_game_logs[n][value] for key, value in team_box_cols.items()] for n, i in enumerate(league_game_logs)]
        insert_content = str(team_boxes)[1:-1].replace("[", "(").replace("]", ")").replace("None", "Null").replace('"', "'")
        conn.execute("INSERT INTO prod.team_box VALUES " + insert_content + " ON CONFLICT DO NOTHING")
        conn.execute("INSERT INTO stage.team_box_clean VALUES " + insert_content)


player_box_cols = OrderedDict({'MIN': 8, 'FGM': 9, 'FGA': 10, 'FG_PCT': 11, 'FG3M': 12, 'FG3A': 13, 'FG3_PCT': 14,
                               'FTM': 15, 'FTA': 16, 'FT_PCT': 17, 'OREB': 18, 'DREB': 19, 'REB': 20, 'AST': 21,
                               'STL': 22, 'BLK': 23, 'TOV': 24, 'PF': 25, 'PTS': 26, 'PLUS_MINUS': 27, 'GAME_ID': 0,
                               'TEAM_ID': 1, 'PLAYER_ID': 4, 'STARTED': 6})


def insert_player_box(**kwargs):
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    player_boxes_stage = session.query(PlayerBoxStage.__table__).filter(PlayerBoxStage.GAME_ID.in_(game_ids_tuple)).all()
    if player_boxes_stage:
        for n, i in enumerate(player_boxes_stage):
            player_boxes_stage[n] = list(i)
        for i in player_boxes_stage:
            if i[8] not in ['0', None]:
                split_time = i[8].split(':')
                i[8] = int(split_time[0])*60 + int(split_time[1]) if len(split_time) == 2 else int(i[8])*60
            else:
                i[8] = 0
            i[6] = True if i[6] not in ['', ' '] else False
        player_boxes = [[player_boxes_stage[n][value] for key, value in player_box_cols.items()] for n, i in enumerate(player_boxes_stage)]
        insert_content = str(player_boxes)[1:-1].replace("[", "(").replace("]", ")").replace("None", "Null").replace('"', "'")
        conn.execute("INSERT INTO prod.player_box VALUES " + insert_content + " ON CONFLICT DO NOTHING")
        conn.execute("INSERT INTO stage.player_box_clean VALUES " + insert_content)


player_season_totals = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
                        'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'SEASON_ID', 'TEAM_ID',
                        'PLAYER_ID', 'GAMES', 'GAMES_STARTED']


def add_season_totals_player(**kwargs):
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    player_boxes = session.query(CleanPlayerBoxStage.__table__).filter(CleanPlayerBoxStage.GAME_ID.in_(game_ids_tuple)).all()
    for n, i in enumerate(player_boxes):
        player_boxes[n] = list(i)
    for player_box in player_boxes:
        game = session.query(LeagueGameLog.__table__).filter(LeagueGameLog.GAME_ID == player_box[-4]).first()
        year = int(game[0][1:])
        season_id = str(year) + '-' + str(year + 1)[-2:]
        playoffs = game[-1]
        team_id = player_box[-3]
        player_id = player_box[-2]
        model = psr if not playoffs else psp
        season = 'post' if playoffs else 'reg'
        active_season_teams = session.query(model.__table__).filter(model.PLAYER_ID == player_id,
                                                                    model.SEASON_ID == season_id).all()
        active_season_team = False
        for active_season in active_season_teams:
            if team_id == active_season[-4]:
                active_season_team = True
                break
        if not active_season_team:
            new_season = tuple([0]*20 + [season_id] + [team_id] + [player_id] + [0] * 2)
            conn.execute("INSERT INTO prod.player_season_{} VALUES ".format(season) + str(new_season))
            active_season_teams.append(new_season)
            total_seasons_teams = len(active_season_teams)
            if total_seasons_teams == 2:
                new_season = list(active_season_teams[0])
                new_season[-4] = 0
                new_season = tuple(new_season)
                conn.execute("INSERT INTO prod.player_season_{} VALUES ".format(season) + str(new_season))
                active_season_teams.append(new_season)
        seasons_to_update = []
        for active_season in active_season_teams:
            if active_season[-4] in [team_id, 0]:
                seasons_to_update.append(active_season)
        for active_season_team in seasons_to_update:
            active_season_team = list(active_season_team)
            for ind in range(20):
                if player_box[ind] is not None:
                    active_season_team[ind] += player_box[ind]
            for ind in [3, 6, 9]:
                if active_season_team[ind-1]:
                    active_season_team[ind] = active_season_team[ind-2]/active_season_team[ind-1]
            if player_box[-1]:
                active_season_team[-1] += 1
            for ind in range(20):
                if active_season_team[ind] not in [0, None]:
                    active_season_team[-2] += 1
                    break
            insert_dict = {key: active_season_team[n] for n, key in enumerate(player_season_totals)}
            conn.execute(update(model.__table__).where(and_(model.PLAYER_ID == player_id,
                                                       model.SEASON_ID == season_id,
                                                       model.TEAM_ID == active_season_team[-4])).values(insert_dict))


team_season_totals = ['MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
                      'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'OPPT_FGM', 'OPPT_FGA',
                      'OPPT_FG_PCT', 'OPPT_FG3M', 'OPPT_FG3A', 'OPPT_FG3_PCT', 'OPPT_FTM', 'OPPT_FTA', 'OPPT_FT_PCT',
                      'OPPT_OREB', 'OPPT_DREB', 'OPPT_REB', 'OPPT_AST', 'OPPT_STL', 'OPPT_BLK', 'OPPT_TOV', 'OPPT_PF',
                      'OPPT_PTS', 'TEAM_ID', 'SEASON_ID', 'GAMES', 'WINS', 'LOSSES']


def add_season_totals_team(**kwargs):
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    team_boxes = session.query(CleanTeamBoxStage.__table__).filter(CleanTeamBoxStage.GAME_ID.in_(game_ids_tuple)).all()
    for n, i in enumerate(team_boxes):
        team_boxes[n] = list(i)
    for team_box in team_boxes:
        game = session.query(LeagueGameLog.__table__).filter(LeagueGameLog.GAME_ID == team_box[-4]).first()
        year = int(game[0][1:])
        season_id = str(year) + '-' + str(year + 1)[-2:]
        playoffs = game[-1]
        team_id = team_box[-5]
        model = tsr if not playoffs else tsp
        season = 'post' if playoffs else 'reg'
        oppt_team_box = list(session.query(CleanTeamBoxStage.__table__).filter(CleanTeamBoxStage.GAME_ID == team_box[-4],
                                                                               CleanTeamBoxStage.TEAM_ID == team_box[-1]).one())
        active_season_team = session.query(model.__table__).filter(model.SEASON_ID == season_id,
                                                                   model.TEAM_ID == team_id).first()
        if not active_season_team:
            new_season = tuple([0]*38 + [team_id] + [season_id] + [0] * 3)
            conn.execute("INSERT INTO prod.team_season_{} VALUES ".format(season) + str(new_season))
            active_season_team = new_season
        active_season_team = list(active_season_team)
        for ind in range(20):
            if team_box[ind] is not None:
                active_season_team[ind] += team_box[ind]
        for ind in range(20, 38):
            if oppt_team_box[ind-19] is not None:
                active_season_team[ind] += oppt_team_box[ind-19]
        for ind in [3, 6, 9, 22, 25, 28]:
            if active_season_team[ind-1]:
                active_season_team[ind] = active_season_team[ind-2]/active_season_team[ind-1]
        if team_box[-2]:
            active_season_team[-2] += 1
        else:
            active_season_team[-1] += 1
        active_season_team[-3] += 1
        insert_dict = {key: active_season_team[n] for n, key in enumerate(team_season_totals)}
        conn.execute(update(model.__table__).where(and_(model.SEASON_ID == season_id,
                                                        model.TEAM_ID == team_id)).values(insert_dict))


def clean_up(**kwargs):
    date = kwargs['ds']
    game_ids_tuple = [i[0] for i in session.query(LeagueGameLog.GAME_ID.distinct()).filter(
        LeagueGameLog.GAME_DATE == date).all()]
    conn.execute(delete(LeagueGameLog.__table__).where(LeagueGameLog.GAME_DATE == date))
    conn.execute(delete(PlayerBoxStage.__table__).where(PlayerBoxStage.GAME_ID.in_(game_ids_tuple)))
    conn.execute(delete(CleanPlayerBoxStage.__table__).where(CleanPlayerBoxStage.GAME_ID.in_(game_ids_tuple)))
    conn.execute(delete(CleanTeamBoxStage.__table__).where(CleanTeamBoxStage.GAME_ID.in_(game_ids_tuple)))


stage_game_logs = PythonOperator(
    task_id="stage_game_logs",
    python_callable=stage_game_logs,
    provide_context=True,
    dag=dag,
)

stage_player_boxes = PythonOperator(
    task_id="stage_player_boxes",
    python_callable=stage_player_boxes,
    provide_context=True,
    dag=dag,
)

insert_new_players = PythonOperator(
    task_id="insert_new_players",
    python_callable=insert_new_players,
    provide_context=True,
    dag=dag,
)

insert_games = PythonOperator(
    task_id="insert_games",
    python_callable=insert_games,
    provide_context=True,
    dag=dag,
)

insert_team_box = PythonOperator(
    task_id="insert_team_box",
    python_callable=insert_team_box,
    provide_context=True,
    dag=dag,
)

insert_player_box = PythonOperator(
    task_id="insert_player_box",
    python_callable=insert_player_box,
    provide_context=True,
    dag=dag,
)

add_season_totals_player = PythonOperator(
    task_id="add_season_totals_player",
    python_callable=add_season_totals_player,
    provide_context=True,
    dag=dag,
)

add_season_totals_team = PythonOperator(
    task_id="add_season_totals_team",
    python_callable=add_season_totals_team,
    provide_context=True,
    dag=dag,
)

clean_up = PythonOperator(
    task_id="clean_up",
    python_callable=clean_up,
    provide_context=True,
    dag=dag,
)

# initialize_db = PythonOperator(
#     task_id='initialize_db',
#     python_callable=initialize_db,
#     dag=dag
# )

stage_game_logs >> [stage_player_boxes, insert_games]
insert_games >> insert_team_box >> add_season_totals_team
stage_player_boxes >> insert_new_players
[insert_games, insert_new_players] >> insert_player_box >> add_season_totals_player
[add_season_totals_team, add_season_totals_player] >> clean_up

# initialize_db


