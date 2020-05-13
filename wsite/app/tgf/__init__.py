from flask import Blueprint

bp = Blueprint('tgf', __name__)

from app.tgf import team_game_finder