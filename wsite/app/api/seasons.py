from app.api import bp
from app.models import *
from flask import jsonify
from app import db
from app.api import bp
from sqlalchemy.orm import aliased
from datetime import datetime


@bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    data = list(db.session.query(Player.__table__).filter(Player.PLAYER_ID == player_id).first_or_404())
    data[4] = str(int(data[4]/12)) + '-' + str(data[4] % 12)
    return jsonify({
        'Headers': Player.__table__.columns.keys(),
        'Data': data
    })


@bp.route('/standings/<season>', methods=['GET'])
def standings(season):
    headers = ["TEAM", "WINS", "LOSSES"]
    data = list(db.session.query(Teams.NAME, TeamSeasonReg.WINS, TeamSeasonReg.LOSSES).join(Teams.__table__)
                .filter(TeamSeasonReg.SEASON_ID == season)
                .order_by(TeamSeasonReg.WINS.desc()).all())
    return jsonify({
        'Headers': headers,
        'Data': data
    })