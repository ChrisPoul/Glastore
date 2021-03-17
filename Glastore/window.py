from flask import (
    Blueprint, render_template
)

bp = Blueprint('window', __name__)

@bp.route('/')
@bp.route('/add_window')
def add_window():

    return render_template(
        'window/add_window.html'
    )
