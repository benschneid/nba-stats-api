from app.pgf import bp
from flask import render_template
from app import db
from app.models import *
from flask import request
from sqlalchemy.orm import aliased
from dateutil.relativedelta import relativedelta
from flask import jsonify
from datetime import datetime
from sqlalchemy.sql import and_


@bp.route('/', methods=['GET'])
def index():
    return render_template('player_game_finder_home.html', title='Player Game Finder')


@bp.route('/find', methods=['GET'])
def finder():
    Oppt_Teams = aliased(Teams)
    dfs = '%Y-%m-%d %H:%M:%S'
    query_args = {}
    for arg in ["Seasons0", "Seasons1", "Age0", "Age1", "Game_Month", "Team", "Opponent", "Game_Result",
                "Role", "Game_Location", "stats0", "stats1", "stats2", "stats3", "operators0", "operators1",
                "operators2", "operators3", "input0", "input1", "input2", "input3", "order"]:
        query_args[arg] = request.args.get(arg)
    headers = ["Rank", "Player", "Date", "Team", "Opponent", "W/L", "GS"] + PlayerBoxProd.__table__.columns.keys()[:-4]
    data = [Player.NAME, Games.GAME_DATE, Teams.NAME, Oppt_Teams.NAME, TeamBox.WIN, PlayerBoxProd.STARTED] + \
           [getattr(PlayerBoxProd, col) for col in headers[7:]]
    player_data = db.session.query(*data).join \
        (Player.__table__).join(Games.__table__, PlayerBoxProd.GAME_ID == Games.GAME_ID).join \
        (TeamBox.__table__, and_(Games.GAME_ID == TeamBox.GAME_ID, PlayerBoxProd.TEAM_ID == TeamBox.TEAM_ID)). join \
        (Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID)

    filter_args = [Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID]
    if query_args["Seasons0"] != "Any":
        filter_args.append(Games.SEASON_ID >= query_args["Seasons0"])
    if query_args["Seasons1"] != "Any":
        filter_args.append(Games.SEASON_ID <= query_args["Seasons1"])
    # if query_args["Age0"] != "Any":
    #     filter_args.append(relativedelta(datetime.strptime(str(Games.GAME_DATE), dfs),
    #                                      datetime.strptime(str(Player.DOB), dfs)).years >= query_args["Age0"])
    # if query_args["Age1"] != "Any":
    #     filter_args.append(relativedelta(datetime.strptime(str(Games.GAME_DATE), dfs),
    #                                      datetime.strptime(str(Player.DOB), dfs)).years <= query_args["Age1"])
    if query_args["Team"] != "Any":
        filter_args.append(PlayerBoxProd.TEAM_ID == int(query_args["Team"]))
    if query_args["Opponent"] != "Any":
        filter_args.append(Oppt_Teams.TEAM_ID == int(query_args["Opponent"]))
    if query_args["Game_Result"] != "Either":
        filter_args.append(TeamBox.WIN == (True if query_args["Game_Result"] == "Won" else False))
    if query_args["Role"] != "Either":
        filter_args.append(PlayerBoxProd.STARTED == (True if query_args["Role"] == "Starter" else False))
    if query_args["Game_Location"] != "Either":
        filter_args.append(TeamBox.HOME == (True if query_args["Game_Location"] == "Home" else False))
    query_results = list(player_data.filter(*filter_args).paginate(per_page=100).items)
    return jsonify(list(query_results))

    # return render_template('player_game_finder_home.html', title='Player Game Finder')