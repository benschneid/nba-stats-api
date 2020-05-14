from app.pgf import bp
from flask import render_template
from app import db
from app.models import *
from flask import request
from sqlalchemy.orm import aliased
from flask import jsonify
from datetime import datetime
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import nullslast
from sqlalchemy import text, extract
import calendar


@bp.route('/', methods=['GET'])
def index():
    return render_template('pgf_home.html', title='Player Game Finder')


@bp.route('/find', methods=['GET'])
def finder():
    Oppt_Teams = aliased(Teams)
    dfs = '%Y-%m-%d %H:%M:%S'
    query_args = {}
    for arg in ["mode", "Seasons0", "Seasons1", "Age0", "Age1", "Game_Month", "Team", "Opponent", "Game_Result",
                "Role", "Game_Location", "stats0", "stats1", "stats2", "stats3", "operators0", "operators1",
                "operators2", "operators3", "input0", "input1", "input2", "input3", "order", "page"]:
        query_args[arg] = request.args.get(arg)
    mode = query_args["mode"]
    if mode == "Single":
        headers = ["Rank", "Player", "Date", "Team", "Opponent", "W/L", "GS"] + PlayerBoxProd.__table__.columns.keys()[:-4]
        data = [Player.NAME, Games.GAME_DATE, Teams.NAME, Oppt_Teams.NAME, TeamBox.WIN, PlayerBoxProd.STARTED] + \
               [getattr(PlayerBoxProd, col) for col in headers[7:]] + [PlayerBoxProd.PLAYER_ID]
        player_data = db.session.query(*data).join \
            (Player.__table__).join(Games.__table__, PlayerBoxProd.GAME_ID == Games.GAME_ID).join \
            (TeamBox.__table__, and_(Games.GAME_ID == TeamBox.GAME_ID, PlayerBoxProd.TEAM_ID == TeamBox.TEAM_ID)).join \
            (Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID)
    else:
        headers = ["Rank", "Player", "Count"]
        player_data = db.session.query(Player.NAME, db.func.count(Player.NAME).label('total'), Player.PLAYER_ID).join \
            (PlayerBoxProd.__table__).join(Games.__table__, PlayerBoxProd.GAME_ID == Games.GAME_ID).join \
            (TeamBox.__table__, and_(Games.GAME_ID == TeamBox.GAME_ID, PlayerBoxProd.TEAM_ID == TeamBox.TEAM_ID)).join \
            (Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID)
    search_text = "Current search: In a single game" if mode == "Single" else "Current search: In multiple seasons"
    filter_args = [Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID]
    if query_args["Seasons0"] != "Any":
        filter_args.append(Games.SEASON_ID >= query_args["Seasons0"])
        search_text += ", from {}".format(query_args["Seasons0"])
    if query_args["Seasons1"] != "Any":
        filter_args.append(Games.SEASON_ID <= query_args["Seasons1"])
        search_text += ", until {}".format(query_args["Seasons1"])
    if query_args["Game_Month"] != "Any":
        filter_args.append(extract('month', Games.GAME_DATE) == int(query_args["Game_Month"]))
        search_text += ", in month {}".format(calendar.month_name[int(query_args["Game_Month"])])
    if query_args["Age0"] != "Any":
        search_text += ", player older than {}".format(query_args["Age0"])
        filter_args.append(Games.GAME_DATE - Player.DOB >= text("INTERVAL '{} YEAR'".format(query_args["Age0"])))
    if query_args["Age1"] != "Any":
        filter_args.append(Games.GAME_DATE - Player.DOB <= text("INTERVAL '{} YEAR'".format(query_args["Age1"])))
        search_text += ", player younger than {}".format(query_args["Age1"])
    if query_args["Team"] != "Any":
        filter_args.append(Teams.NAME == query_args["Team"])
        search_text += ", playing for {}".format(query_args["Team"])
    if query_args["Opponent"] != "Any":
        filter_args.append(Oppt_Teams.NAME == query_args["Opponent"])
        search_text += ", against {}".format(query_args["Opponent"])
    if query_args["Game_Result"] != "Either":
        filter_args.append(TeamBox.WIN == (True if query_args["Game_Result"] == "Won" else False))
        search_text += ", {} game".format(query_args["Game_Result"].lower())
    if query_args["Role"] != "Either":
        filter_args.append(PlayerBoxProd.STARTED == (True if query_args["Role"] == "Starter" else False))
        search_text += ", played as {}".format(query_args["Role"].lower())
    if query_args["Game_Location"] != "Either":
        filter_args.append(TeamBox.HOME == (True if query_args["Game_Location"] == "Home" else False))
        search_text += ", game played at {}".format(query_args["Game_Location"])
    if query_args["Game_Type"] != "Either":
        filter_args.append(Games.PLAYOFFS == (True if query_args["Game_Type"] == "Playoffs" else False))
        search_text += ", game played at {}".format(query_args["Game_Location"])
    for i in range(4):
        s = str(i)
        if query_args["input"+s] and query_args["stats"+s] != "Any":
            if query_args["operators"+s] == "gt":
                filter_args.append(getattr(PlayerBoxProd, query_args["stats"+s]) >= float(query_args["input"+s]))
                search_text += ", {} >= {}".format(query_args["stats"+s], query_args["input"+s])
            else:
                filter_args.append(getattr(PlayerBoxProd, query_args["stat" + s]) <= float(query_args["input" + s]))
                search_text += ", {} <= {}".format(query_args["stats" + s], query_args["input" + s])
    page = int(query_args["page"])
    if mode == "Single":
        query_results = player_data.filter(*filter_args).order_by\
            (nullslast(getattr(PlayerBoxProd, query_args["order"]).desc())).paginate\
            (page=page, per_page=100, error_out=True)
    else:
        query_results = player_data.filter(*filter_args).group_by(Player.NAME, Player.PLAYER_ID).order_by\
            (text('total DESC')).paginate\
            (page=page, per_page=100, error_out=True)
    search_text += ", sorted by {}.".format(query_args["order"] if mode == "Single" else "most games matching criteria")
    query_results_list = [list(i) for i in query_results.items]
    if mode == "Single":
        for n, row in enumerate(query_results_list):
            row.insert(0, n+1+(page-1)*100)
            row[7] = int(row[7] / 60)
            row[5] = 'W' if row[5] else 'L'
            row[6] = 1 if row[6] else 0
            row[2] = datetime.strftime(row[2], '%m-%d-%Y')
            for i in [10, 13, 16]:
                if row[i]:
                    row[i] = round(row[i], 3)
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = 0

        for i in [10, 13, 16]:
            headers[i] = headers[i].replace("_", " ")
        headers[len(headers) - 1] = "+/-"
    else:
        for n, row in enumerate(query_results_list):
            row.insert(0, n + 1 + (page - 1) * 100)
    col = headers.index(query_args["order"]) if mode == "Single" else headers.index("Count")
    return render_template('pgf_data.html', search_text=search_text,
                           title='Player Game Finder', headers=headers,
                           data_dict=query_results_list, col=col,
                           has_prev=query_results.has_prev, has_next=query_results.has_next,
                           page=page)
