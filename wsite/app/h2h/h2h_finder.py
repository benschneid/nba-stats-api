from app.h2h import bp
from flask import render_template
from app import db
from app.models import *
from flask import request
from sqlalchemy.orm import aliased
from flask import jsonify
from datetime import datetime
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import nullslast
from sqlalchemy import text, extract, func
import calendar


@bp.route('/', methods=['GET'])
def index():
    return render_template('h2h_home.html', title='Head2Head Finder')


@bp.route('/find', methods=['GET'])
def finder():
    dfs = '%Y-%m-%d %H:%M:%S'
    player1 = request.args.get("player1")
    player2 = request.args.get("player2")
    player1_name = db.session.query(Player.NAME).filter(Player.PLAYER_ID == player1).first_or_404()[0]
    player2_name = db.session.query(Player.NAME).filter(Player.PLAYER_ID == player2).first_or_404()[0]
    games = [row[0] for row in list(db.session.query(PlayerBoxProd.GAME_ID)
                                    .filter(or_(PlayerBoxProd.PLAYER_ID == player1, PlayerBoxProd.PLAYER_ID == player2),
                                            PlayerBoxProd.MIN > 0)
                                    .group_by(PlayerBoxProd.GAME_ID)
                                    .having(func.count(PlayerBoxProd.GAME_ID) == 2).all())]
    same_team = [row[0] for row in list(db.session.query(PlayerBoxProd.GAME_ID)
                                        .filter(or_(PlayerBoxProd.PLAYER_ID == player1, PlayerBoxProd.PLAYER_ID == player2),
                                                PlayerBoxProd.MIN > 0)
                                        .group_by(PlayerBoxProd.GAME_ID, PlayerBoxProd.TEAM_ID)
                                        .having(func.count(PlayerBoxProd.GAME_ID) == 2).all())]
    for i in same_team:
        if i in games:
            games.remove(i)
    headers = ['Rk', 'Player', 'Date', 'Team'] + PlayerBoxProd.__table__.columns.keys()[:-4]
    data = [Player.NAME, Games.GAME_DATE, Teams.NAME] + [getattr(PlayerBoxProd, i) for i in headers[4:]]
    player_data_reg = list(db.session.query(*data)
                           .join(Games.__table__, PlayerBoxProd.GAME_ID == Games.GAME_ID)
                           .join(Player.__table__, PlayerBoxProd.PLAYER_ID == Player.PLAYER_ID)
                           .join(Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID)
                           .filter(Games.GAME_ID.in_(games), Games.PLAYOFFS == False,
                                   PlayerBoxProd.PLAYER_ID.in_([player1, player2]))
                           .order_by(Games.GAME_DATE.desc(), Player.NAME.desc()).all())
    player_data_post = list(db.session.query(*data)
                            .join(Games.__table__, PlayerBoxProd.GAME_ID == Games.GAME_ID)
                            .join(Player.__table__, PlayerBoxProd.PLAYER_ID == Player.PLAYER_ID)
                            .join(Teams.__table__, PlayerBoxProd.TEAM_ID == Teams.TEAM_ID)
                            .filter(Games.GAME_ID.in_(games),
                                    PlayerBoxProd.PLAYER_ID.in_([player1, player2]), Games.PLAYOFFS == True)
                            .order_by(Games.GAME_DATE.desc(), Player.NAME.desc()).all())

    player_data_reg = [list(row) for row in player_data_reg]
    player_data_post = [list(row) for row in player_data_post]
    for table in [player_data_reg, player_data_post]:
        for n, row in enumerate(table):
            row.insert(0, n+1)
            row[2] = datetime.strftime(row[2], '%m-%d-%Y')
            row[4] = str(int(row[4]/60)) + ':' + str(row[4] % 60).zfill(2)
    for n, i in enumerate(headers):
        headers[n] = headers[n].replace("_", " ").replace('PCT', '%')
    return render_template('h2h_data.html',
                           title='{} vs. {}'.format(player1_name, player2_name), headers=headers,
                           reg_dict=player_data_reg, post_dict=player_data_post)







