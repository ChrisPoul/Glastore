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
        self.error = None
        self.validate_name()
        self.validate_email()
        if not self.error:
            self.error = add_to_db(self)

        return self.error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
                    self.error = "El nombre del cliente no puede llevar numeros, solo letras"
                    break

    def validate_email(self):
        if not self.error:
            if self.email:
                if "@" not in self.email:
                    self.error = "El correo que introdujo es invalido"


def init_db():
    db.drop_all()
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
        error = "Introdujo un valor que ya está en uso"
        db.session.rollback()

    return error


def add_to_db(item):
    db.session.add(item)
    error = commit_to_db()

    return error
