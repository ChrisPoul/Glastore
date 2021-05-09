import functools
from flask import session, g, request
from . import User


class UserAuth:

    def register(self):
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        error = None

        if not email:
            error = "Es necesario proporcionar un correo valido"        
        elif not username:
            error = "El nombre de usuario es requerido"
        elif not password:
            error = "Contraseña requerida"

        if not error:
            user = User(
                email=email,
                username=username,
                password=password
            )
            try:
                user.add()
            except ValueError:
                error = "Eso no está disponible"

        return error

    def login(self):
        username_email = request.form['username_email']
        password = request.form['password']
        error = None

        user = User.search(username_email)
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
