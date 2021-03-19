from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash
)
from Glastore.models import Window
from Glastore import get_form

bp = Blueprint('window', __name__, url_prefix='/window')

window_heads = {
    "name": "Nombre",
    "description": "Descripción",
    "material": "Material",
    "color": "Color",
    "cristal": "Cristal",
    "acabado": "Acabado",
    "modelo": "Modelo",
    "herrajes": "Herrajes",
    "sellado": "Sellado"
}


@bp.route('/windows')
def windows():
    windows = Window.get_all()

    return render_template(
        'window/windows.html',
        heads=window_heads,
        windows=windows
    )


@bp.route('/add', methods=('GET', 'POST'))
def add():
    form = get_form()

    if request.method == "POST":
        form = get_form(window_heads)
        window = Window(
            name=form["name"],
            description=form["description"],
            material=form["material"],
            color=form["color"],
            cristal=form["cristal"],
            acabado=form["acabado"],
            modelo=form["modelo"],
            herrajes=form["herrajes"],
            sellado=form["sellado"]
        )
        error = window.add()

        if not error:
            return redirect(
                url_for('window.windows')
            )
        flash(error)

    return render_template(
        'window/add.html',
        heads=window_heads,
        form=form
    )


@bp.route('/update/<int:window_id>', methods=('POST', 'GET'))
def update(window_id):
    window = Window.get(window_id)

    if request.method == 'POST':
        window.name = request.form["name"]
        window.description = request.form["description"]
        window.material = request.form["material"]
        window.color = request.form["color"]
        window.cristal = request.form["cristal"]
        window.acabado = request.form["acabado"]
        window.modelo = request.form["modelo"]
        window.herrajes = request.form["herrajes"]
        window.sellado = request.form["sellado"]
        error = window.update()

        if not error:
            return redirect(
                url_for('window.windows')
            )
        flash(error)

    return render_template(
        'window/update.html',
        heads=window_heads,
        window=window
    )
