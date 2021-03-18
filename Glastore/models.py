import click
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


class Customer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    address = Column(String(150), nullable=True, unique=True)
    cotizacion = Column(String(100), nullable=True, unique=True)

    def __repr__(self):
        return self.__dict__

    def add(self):
        error = None

        nums = "1234567890"
        for num in nums:
            if num in self.name:
                error = "El nombre del cliente no puede llevar numeros, solo letras"
                break

        if self.email:
            if "@" not in self.email:
                error = "El correo que introdujiste es invalido"

        if not error:
            error = add_to_db(self)

        return error


def init_db():
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized Database')


def add_to_db(item):
    db.session.add(item)
    error = None
    try:
        db.session.commit()
    except IntegrityError:
        error = "Introdujo un valor que ya está en uso"

    return error
