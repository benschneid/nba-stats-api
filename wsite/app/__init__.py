from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
db = SQLAlchemy()
bootstrap = Bootstrap()
from app.models import *


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap.init_app(app)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    from app.pgf import bp as pgf_bp
    app.register_blueprint(pgf_bp, url_prefix='/pgf')
    #
    # @app.route('/', defaults={'path': ''})
    # @app.route('/<path:path>')
    # def catch_all(path):
    #     return 'You want path: %s' % path

    @app.context_processor
    def context_processor():
        player_data = db.session.query(Player.NAME, Player.FROM_YEAR, Player.TO_YEAR, Player.PLAYER_ID).all()
        players = [player[0] for player in player_data]
        from_years = [player[1] for player in player_data]
        to_years = [player[2] for player in player_data]
        ids = [player[3] for player in player_data]
        return dict(players=players, from_years=from_years, to_years=to_years, ids=ids)

    return app

