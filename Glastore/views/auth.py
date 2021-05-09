import functools
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g
)
from Glastore.models.user.auth import UserAuth

bp = Blueprint("auth", __name__, url_prefix="/auth")

register_heads = {
    "email": "Correo electrónico",
    "username": "Nombre de usuario",
    "password": "Contraseña"
}
login_heads = {
    "username_email": "Nombre de usuario o correo electrónico",
    "password": "Contraseña"
}


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user_auth = UserAuth()
        error = user_auth.register()

        if not error:
            return redirect(
                url_for('auth.login')
            )

        flash(error)

    return render_template(
        'auth/register.html',
        heads=register_heads
    )


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == "POST":
        user_auth = UserAuth()
        error = user_auth.login()

        if not error:
            return redirect(
                url_for('home.home')
            )
        
        flash(error)
    
    return render_template(
        'auth/login.html',
        heads=login_heads
    )


@bp.route('/logout')
def logout():
    user_auth = UserAuth()
    user_auth.logout()
    return redirect(
        url_for('auth.login')
    )


@bp.before_app_request
def load_loged_in_user():
    user_auth = UserAuth()
    user_auth.load_loged_in_user()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(
                url_for('auth.login')
            )
        return view(**kwargs)
    
    return wrapped_view
