from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home', form=None,
                           posts=None, next_url=None,
                           prev_url=None)

