from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from Glastore.interactors.user import UserInteractor

bp = Blueprint("auth", __name__, url_prefix="/auth")

user_heads = {
    "username": "Nombre de Usuario",
    "password": "Contraseña"
}


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        interactor = UserInteractor(request)
        error = interactor.register()

        if not error:
            return redirect(
                url_for('auth.login')
            )

        flash(error)

    return render_template(
        'auth/register.html',
        heads=user_heads
    )


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        interactor = UserInteractor(request)
        error = interactor.login()

        if not error:
            return redirect(
                url_for('home.home')
            )
    
    return render_template(
        'auth/login.html'
    )
