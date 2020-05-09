from app.pgf import bp
from flask import render_template
from app import db
from app.models import *


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('player_game_finder_home.html', title='Player Game Finder')