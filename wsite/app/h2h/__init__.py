from flask import Blueprint

bp = Blueprint('h2h', __name__)

from app.h2h import h2h_finder