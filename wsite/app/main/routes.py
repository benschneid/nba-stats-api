from app.main import bp
from flask import render_template
from app import db
from app.models import *
import copy


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')


@bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About')


@bp.route('/players/<int:player_id>')
def player_page(player_id):
    player_info = list(db.session.query(Player.__table__).filter(Player.PLAYER_ID == player_id).first_or_404())
    name = player_info[1]
    headers = ["SEASON", "TEAM", "G", "GS"] + PlayerSeasonReg.__table__.columns.keys()[:-5]
    data_dict = {}
    for player_season in [PlayerSeasonReg, PlayerSeasonPost]:
        data = [getattr(player_season, "SEASON_ID"), getattr(Teams, "NAME"),
                getattr(player_season, "GAMES"), getattr(player_season, "GAMES_STARTED")]
        for i in range(4, len(headers)):
            data.append(getattr(player_season, headers[i]))
        player_data = list(db.session.query\
            (*data).join(Teams.__table__).filter\
            (player_season.PLAYER_ID == player_id).order_by(player_season.SEASON_ID).all())
        player_data = [list(i) for i in player_data]
        player_data_pergame = copy.deepcopy(player_data)
        player_data_per36 = copy.deepcopy(player_data)
        for n, table in enumerate([player_data_pergame, player_data_per36]):
            for row in table:
                for i in [5, 6, 8, 9] + [i for i in range(11, len(headers))] + [4]:
                    if n == 0:
                        if row[2] != 0:
                            row[i] = row[i] / row[2]
                    else:
                        if row[4] != 0:
                            row[i] = row[i] / row[4] * 36 * 60
        for table in [player_data, player_data_pergame, player_data_per36]:
            for row in table:
                row[4] = round(row[4]/60, 1)
                for i in [7,10,13]:
                    row[i] = round(row[i], 3)
                for i in [5, 6, 8, 9] + [i for i in range(11, len(headers))]:
                    row[i] = round(row[i], 1)

        if player_season == PlayerSeasonReg:
            data_dict['Regular Season Totals'] = player_data
            data_dict['Regular Season Per Game'] = player_data_pergame
            data_dict['Regular Season Per 36'] = player_data_per36
        else:
            data_dict['Posteason Totals'] = player_data
            data_dict['Posteason Per Game'] = player_data_pergame
            data_dict['Posteason Per 36'] = player_data_per36
    for i in [7,10,13,len(headers)-1]:
        headers[i] = headers[i].replace("_", " ")
    return render_template('player_page.html', title=name + ' Stats', headers=headers, data_dict=data_dict, name=name)
