import functools
from flask import session, g, request
from . import User


class UserAuth:

    def register(self):
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = "Nombre de usuario requerido"
        elif not password:
            error = "Contraseña requerida"
        elif User.search(username) is not None:
            error = "That username is already in use"

        if not error:
            user = User(
                username=username,
                password=password
            )
            user.add()

        return error

    def login(self):
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.search(username)
        if not user:
            error = "Incorrect Username"
        elif password != user.password:
            error = "Incorrect Password"

        if not error:
            session.clear()
            session['user_id'] = user.id

        return error

    def logout(self):
        session.clear()

    def load_loged_in_user(self):
        try:
            user_id = session["user_id"]
        except KeyError:
            user_id = None

        if user_id is None:
            g.user = None
        else:
            g.user = User.get(user_id)
