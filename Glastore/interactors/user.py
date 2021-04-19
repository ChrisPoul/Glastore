from flask import session
from Glastore.models.user import User


class UserInteractor:

    def __init__(self, request):
        self.request = request

    def register(self):
        username = self.request.form['username']
        password = self.request.form['password']
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
        username = self.request.form['username']
        password = self.request.form['password']
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
