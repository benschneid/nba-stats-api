from app.api import bp
from app.models import *
from flask import jsonify
from app import db
from app.api import bp


@bp.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    return jsonify({
        'Headers': Player.__table__.columns.keys(),
        'Data': db.session.query(Player.__table__).filter(Player.PLAYER_ID == player_id).one()
    })


@bp.route('/box_score/<game_id>', methods=['GET'])
def team_box(game_id):
    return jsonify({
            'Headers': PlayerBoxProd.__table__.columns.keys(),
            'Data': db.session.query(
                PlayerBoxProd.__table__, Teams.NAME).join(
                Teams.__table__).filter(PlayerBoxProd.GAME_ID == game_id).order_by(Teams.NAME).all()
        })

