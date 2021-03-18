import click
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String
)
from Glastore import db


class Customer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=False)
    address = Column(String(150), nullable=True, unique=False)

    def __repr__(self):
        return self.__dict__


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
    db.commit()
