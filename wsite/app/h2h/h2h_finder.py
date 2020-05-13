from app.h2h import bp
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
    return render_template('h2h_home.html', title='Head2Head Finder')