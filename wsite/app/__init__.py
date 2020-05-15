from flask import Flask, render_template
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
    from app.tgf import bp as tgf_bp
    app.register_blueprint(tgf_bp, url_prefix='/tgf')
    from app.h2h import bp as h2h_bp
    app.register_blueprint(h2h_bp, url_prefix='/h2h')
    #
    # @app.route('/', defaults={'path': ''})
    # @app.route('/<path:path>')
    # def catch_all(path):
    #     return 'You want path: %s' % path

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('errors/404.html', title="404 Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        # note that we set the 404 status explicitly
        return render_template('errors/500.html', title="500 Internal Server Error"), 500

    @app.context_processor
    def context_processor():
        player_data = db.session.query(Player.NAME, Player.FROM_YEAR, Player.TO_YEAR, Player.PLAYER_ID).all()
        players = [player[0] for player in player_data]
        from_years = [player[1] for player in player_data]
        to_years = [player[2] for player in player_data]
        ids = [player[3] for player in player_data]
        return dict(players=players, from_years=from_years, to_years=to_years, ids=ids)

    return app

