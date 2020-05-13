from app.tgf import bp
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
    return render_template('tgf_home.html', title='Team Game Finder')


@bp.route('/find', methods=['GET'])
def finder():
    Oppt_Teams = aliased(Teams)
    Oppt_Box = aliased(TeamBox)
    dfs = '%Y-%m-%d %H:%M:%S'
    query_args = {}
    for arg in ["mode", "Seasons0", "Seasons1", "Overtime", "Game_Month", "Team", "Opponent", "Game_Result",
                "Game_Location", "stats0", "stats1", "stats2", "stats3", "operators0", "operators1",
                "operators2", "operators3", "input0", "input1", "input2", "input3", "order", "page"]:
        query_args[arg] = request.args.get(arg)
    mode = query_args["mode"]
    if mode == "Single":
        headers = ["Rk", "Date", "Tm", "Opp", "W/L", 'MIN'] + ['PTS', 'FG', "FGA", "FG_PCT", 'FG3M', 'FG3A', 'FG3_PCT',
                                                               'FT', 'FTA', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV'] + \
                  ['OPPT_PTS', 'OPPT_FG', "OPPT_FGA", "OPPT_FG_PCT", 'OPPT_FG3M', 'OPPT_FG3A', 'OPPT_FG3_PCT',
                   'OPPT_FT', 'OPPT_FTA', 'OPPT_FT_PCT', 'OPPT_REB', 'OPPT_AST', 'OPPT_STL', 'OPPT_BLK', 'OPPT_TOV']
        cols = ['MIN', 'PTS', "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", 'REB',
                'AST', 'STL', 'BLK', 'TOV']
        data = [Games.GAME_DATE, Teams.NAME, Oppt_Teams.NAME, TeamBox.WIN] + \
               [getattr(TeamBox, col) for col in cols] + [getattr(Oppt_Box, col) for col in cols[1:]]
        team_data = db.session.query(*data).join(Oppt_Box.__table__, and_(TeamBox.GAME_ID == Oppt_Box.GAME_ID,
                                                 TeamBox.OPPONENT_TEAM_ID == Oppt_Box.TEAM_ID)).join \
            (Games.__table__, TeamBox.GAME_ID == Games.GAME_ID).join \
            (Teams.__table__, TeamBox.TEAM_ID == Teams.TEAM_ID)
    else:
        headers = ["Rank", "Team", "Count"]
        team_data = db.session.query(Teams.NAME, db.func.count(Teams.NAME).label('total'))\
            .join(TeamBox.__table__, Teams.TEAM_ID == TeamBox.TEAM_ID) \
            .join(Games.__table__, TeamBox.GAME_ID == Games.GAME_ID)
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
    if query_args["Team"] != "Any":
        filter_args.append(Teams.NAME == query_args["Team"])
        search_text += ", playing for {}".format(query_args["Team"])
    if query_args["Opponent"] != "Any":
        filter_args.append(Oppt_Teams.NAME == query_args["Opponent"])
        search_text += ", against {}".format(query_args["Opponent"])
    if query_args["Game_Result"] != "Either":
        filter_args.append(TeamBox.WIN == (True if query_args["Game_Result"] == "Won" else False))
        search_text += ", {} game".format(query_args["Game_Result"].lower())
    if query_args["Game_Location"] != "Either":
        filter_args.append(TeamBox.HOME == (True if query_args["Game_Location"] == "Home" else False))
        search_text += ", game played at {}".format(query_args["Game_Location"])
    if query_args["Overtime"] != "Either":
        filter_args.append(TeamBox.MIN > 240 if query_args["Overtime"] == "Yes" else TeamBox.MIN <= 240)
        search_text += ", game played at {}".format(query_args["Game_Location"])
    for i in range(4):
        s = str(i)
        if query_args["input"+s] and query_args["stats"+s] != "Any":
            if query_args["operators"+s] == "gt":
                filter_args.append(getattr(Oppt_Box if query_args["stats"+s].startswith("OPPT") else TeamBox, query_args["stats"+s]) >= float(query_args["input"+s]))
                search_text += ", {} >= {}".format(query_args["stats"+s], query_args["input"+s])
            else:
                filter_args.append(getattr(Oppt_Box if query_args["stats"+s].startswith("OPPT") else TeamBox, query_args["stat" + s]) <= float(query_args["input" + s]))
                search_text += ", {} <= {}".format(query_args["stats" + s], query_args["input" + s])
    page = int(query_args["page"])
    if mode == "Single":
        query_results = team_data.filter(*filter_args).order_by\
            (nullslast(getattr(Oppt_Box if query_args["order"].startswith("OPPT") else TeamBox, query_args["order"][5:] if
            query_args["order"].startswith("OPPT") else query_args["order"]).desc())).paginate\
            (page=page, per_page=100, error_out=True)
    else:
        query_results = team_data.filter(*filter_args).group_by(Teams.NAME).order_by\
            (text('total DESC')).paginate\
            (page=page, per_page=100, error_out=True)
    search_text += ", sorted by {}.".format(query_args["order"] if mode == "Single" else "most games matching criteria")
    query_results_list = [list(i) for i in query_results.items]
    col = headers.index(query_args["order"]) if mode == "Single" else headers.index("Count")
    if mode == "Single":
        for n, row in enumerate(query_results_list):
            row.insert(0, n+1+(page-1)*100)
            row[4] = 'W' if row[4] else 'L'
            row[1] = datetime.strftime(row[1], '%m-%d-%Y')
            for i in [8, 11, 14]:
                if row[i]:
                    row[i] = round(row[i], 3)
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = 0
        for n, i in enumerate(headers):
            if i == "PLUS_MINUS":
                headers[n] = "+/-"
            headers[n] = headers[n].replace("_", " ").replace(" PCT", "%").replace("FG3", "3P").replace("OPPT", "")
    else:
        for n, row in enumerate(query_results_list):
            row.insert(0, n + 1 + (page - 1) * 100)
    return render_template('tgf_data.html', search_text=search_text,
                           title='Team Game Finder', headers=headers,
                           data_dict=query_results_list, col=col,
                           has_prev=query_results.has_prev, has_next=query_results.has_next,
                           page=page)
