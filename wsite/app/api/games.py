from app.api import bp
from app.models import *
from flask import jsonify
from app import db
from app.api import bp
from sqlalchemy.orm import aliased
from datetime import datetime
from sqlalchemy.sql import and_


@bp.route('/player_box/<game_id>', methods=['GET'])
def player_box(game_id):
    game = db.session.query(Games.GAME_ID).filter(Games.GAME_ID == game_id).first_or_404()
    headers = ["GAME_ID", "PLAYER_NAME", "PLAYER_ID", "TEAM_NAME", "TEAM_ID",
               "STARTED"] + PlayerBoxProd.__table__.columns.keys()[:-4]
    pbox_inds = [0, 2] + [i for i in range(5, len(headers))]
    data = []
    for i in pbox_inds:
        data.append(getattr(PlayerBoxProd, headers[i]))
    data.insert(1, getattr(Player, "NAME"))
    data.insert(3, getattr(Teams, "NAME"))
    data.insert(4, getattr(Teams, "TEAM_ID"))
    data = list(db.session.query(*data).join(Teams.__table__).join(Player.__table__).filter(
                PlayerBoxProd.GAME_ID == game_id).order_by(Teams.NAME, PlayerBoxProd.STARTED.desc()).all())
    for i, line in enumerate(data):
        data[i] = list(line)
        data[i][6] = str(int(data[i][6]/60)) + ':' + str(data[i][6] % 60).zfill(2)
    return jsonify({
            'Headers': headers,
            'Data': data
        })


@bp.route('/team_box/<game_id>', methods=['GET'])
def team_box(game_id):
    game = db.session.query(Games.GAME_ID).filter(Games.GAME_ID == game_id).first_or_404()
    Oppt_Teams = aliased(Teams)
    headers = ["GAME_ID", "TEAM_NAME", "TEAM_ID", "HOME", "WIN", "OPPONENT"] + TeamBox.__table__.columns.keys()[:-5]
    tbox_inds = [0, 2, 3, 4] + [i for i in range(6, len(headers))]
    data = []
    for i in tbox_inds:
        data.append(getattr(TeamBox, headers[i]))
    data.insert(1, getattr(Teams, "NAME"))
    data.insert(5, getattr(Oppt_Teams, "NAME"))
    data = list(db.session.query(*data).
                join(Teams.__table__, TeamBox.TEAM_ID == Teams.TEAM_ID)
                .filter(TeamBox.GAME_ID == game_id, Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID).order_by(TeamBox.HOME).all())
    return jsonify({
            'Headers': headers,
            'Data': data
        })


@bp.route('/league_game_log/<season>/<int:playoffs>/<date_from>/<date_to>', methods=['GET'])
def league_game_log(season, playoffs, date_from, date_to):
    Oppt_Teams = aliased(Teams)
    date_format_str = '%m-%d-%Y'
    date_from = datetime.strptime(date_from, date_format_str)
    date_to = datetime.strptime(date_to, date_format_str)
    headers = Games.__table__.columns.keys() + ["TEAM_NAME", "TEAM_ID", "HOME", "WIN", "OPPONENT"] + \
              TeamBox.__table__.columns.keys()[:-5]
    data = []
    for i in range(0, 4):
        data.append(getattr(Games, headers[i]))
    tbox_inds = [5,6,7] + [i for i in range(9, len(headers))]
    for i in tbox_inds:
        data.append(getattr(TeamBox, headers[i]))
    data.insert(4, getattr(Teams, "NAME"))
    data.insert(8, getattr(Oppt_Teams, "NAME"))
    games = db.session.query(*data)\
        .join(TeamBox.__table__, Games.GAME_ID == TeamBox.GAME_ID)\
        .join(Teams.__table__, TeamBox.TEAM_ID == Teams.TEAM_ID)\
        .filter(Games.SEASON_ID == season,
                Games.PLAYOFFS == bool(playoffs),
                date_from <= Games.GAME_DATE, Games.GAME_DATE <= date_to,
                Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID).order_by(Games.GAME_ID, TeamBox.HOME,).all()
    return jsonify({
        'Headers': headers,
        'Data': list(games)})


@bp.route('/player_game_log/<player>/<season>/<int:playoffs>/<date_from>/<date_to>', methods=['GET'])
def player_game_log(player, season, playoffs, date_from, date_to):
    Oppt_Teams = aliased(Teams)
    date_format_str = '%m-%d-%Y'
    date_from = datetime.strptime(date_from, date_format_str)
    date_to = datetime.strptime(date_to, date_format_str)
    headers = Games.__table__.columns.keys() + ["PLAYER_NAME", "PLAYER_ID", "TEAM", "HOME", "WIN", "OPPONENT", "STARTED"] + \
              PlayerBoxProd.__table__.columns.keys()[:-5]
    data = []
    for i in range(0, 4):
        data.append(getattr(Games, headers[i]))
    pbox_inds = [5, 10] + [i for i in range(11, len(headers))]
    for i in pbox_inds:
        data.append(getattr(PlayerBoxProd, headers[i]))
    data.insert(4, getattr(Player, "NAME"))
    data.insert(6, getattr(Teams, "NAME"))
    data.insert(7, getattr(TeamBox, "WIN"))
    data.insert(8, getattr(TeamBox, "HOME"))
    data.insert(9, getattr(Oppt_Teams, "NAME"))
    games = db.session.query(*data)\
        .join(PlayerBoxProd.__table__, Games.GAME_ID == PlayerBoxProd.GAME_ID) \
        .join(Player.__table__, PlayerBoxProd.PLAYER_ID == Player.PLAYER_ID) \
        .join(Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID) \
        .join(TeamBox.__table__, and_(Games.GAME_ID == TeamBox.GAME_ID, PlayerBoxProd.TEAM_ID == TeamBox.TEAM_ID)) \
        .filter(Games.SEASON_ID == season, PlayerBoxProd.PLAYER_ID == player,
                Games.PLAYOFFS == bool(playoffs), Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID,
                date_from <= Games.GAME_DATE, Games.GAME_DATE <= date_to).order_by(Games.GAME_DATE).all()
    return jsonify({
        'Headers': headers,
        'Data': list(games)})


@bp.route('/team_game_log/<int:team>/<season>/<int:playoffs>/<date_from>/<date_to>', methods=['GET'])
def team_game_log(team, season, playoffs, date_from, date_to):
    Oppt_Teams = aliased(Teams)
    date_format_str = '%m-%d-%Y'
    date_from = datetime.strptime(date_from, date_format_str)
    date_to = datetime.strptime(date_to, date_format_str)
    headers = Games.__table__.columns.keys() + ["TEAM_NAME", "TEAM_ID", "HOME", "WIN", "OPPONENT"] + \
              TeamBox.__table__.columns.keys()[:-5]
    data = []
    for i in range(0, 4):
        data.append(getattr(Games, headers[i]))
    tbox_inds = [5, 6, 7] + [i for i in range(9, len(headers))]
    for i in tbox_inds:
        data.append(getattr(TeamBox, headers[i]))
    data.insert(4, getattr(Teams, "NAME"))
    data.insert(8, getattr(Oppt_Teams, "NAME"))
    games = db.session.query(*data)\
        .join(TeamBox.__table__, Games.GAME_ID == TeamBox.GAME_ID)\
        .join(Teams.__table__, TeamBox.TEAM_ID == Teams.TEAM_ID)\
        .filter(Games.SEASON_ID == season,
                Games.PLAYOFFS == bool(playoffs),
                Teams.TEAM_ID == team,
                date_from <= Games.GAME_DATE, Games.GAME_DATE <= date_to,
                Oppt_Teams.TEAM_ID == TeamBox.OPPONENT_TEAM_ID).order_by(Games.GAME_DATE).all()
    return jsonify({
        'Headers': headers,
        'Data': list(games)})