import click
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String, Text,
    PickleType
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
repeated_value_msg = "Introdujo un valor que ya está en uso"


class Customer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    address = Column(String(150), nullable=True, unique=True)
    cotizacion = Column(String(100), nullable=True, unique=True)

    invalid_name_msg = "El nombre del cliente no puede llevar numeros, solo letras"
    invalid_email_msg = "El correo que introdujo es invalido"

    def __repr__(self):
        return self.__dict__

    def add(self):
        self.error = None
        self.validate_name()
        self.validate_email()
        if not self.error:
            self.error = add_to_db(self)

        return self.error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        self.error = None
        self.validate_name()
        self.validate_email()
        if not self.error:
            self.error = commit_to_db()

        return self.error

    def validate_name(self):
        if not self.error:
            nums = "1234567890"
            for num in nums:
                if num in self.name:
                    self.error = self.invalid_name_msg
                    break

    def validate_email(self):
        if not self.error:
            if self.email:
                if "@" not in self.email:
                    self.error = self.invalid_email_msg

    def get(search_term):
        customer = Customer.query.get(search_term)
        if not customer:
            customer = Customer.query.filter_by(name=search_term).first()
        if not customer:
            customer = Customer.query.filter_by(email=search_term).first()
        if not customer:
            customer = Customer.query.filter_by(address=search_term).first()
        if not customer:
            customer = Customer.query.filter_by(cotizacion=search_term).first()

        return customer

    def get_all():
        return Customer.query.all()


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True, unique=False)
    material = Column(String(100), nullable=True, unique=False)
    color = Column(String(100), nullable=True, unique=False)
    cristal = Column(String(100), nullable=True, unique=False)
    acabado = Column(String(100), nullable=True, unique=False)
    modelo = Column(String(100), nullable=True, unique=False)
    herrajes = Column(PickleType, nullable=False, unique=False, default=[])
    sellado = Column(String(100), nullable=True, unique=False)

    def __repr__(self):
        return self.__dict__

    def add(self):
        error = add_to_db(self)
        return error

    def update(self):
        error = commit_to_db()
        return error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get(search_term):
        window = Window.query.get(search_term)
        if not window:
            window = Window.query.filter_by(name=search_term).first()

        return window

    def get_all(search_term=None):
        if search_term:
            windows = Window.query.filter_by(modelo=search_term).all()
            if not windows:
                windows = Window.query.filter_by(cristal=search_term).all()
            if not windows:
                windows = Window.query.filter_by(acabado=search_term).all()
            if not windows:
                windows = Window.query.filter_by(material=search_term).all()
            if not windows:
                windows = Window.query.filter_by(sellado=search_term).all()
            if not windows:
                windows = Window.query.filter_by(color=search_term).all()
        else:
            windows = Window.query.all()

        return windows


def init_db():
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized Database')


def commit_to_db():
    error = None
    try:
        db.session.commit()
    except IntegrityError:
        error = repeated_value_msg
        db.session.rollback()

    return error


def add_to_db(item):
    db.session.add(item)
    error = commit_to_db()

    return error
