import click
from flask import request
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()
repeated_value_msg = "Introdujo un valor que ya está en uso"


def init_db():
    from .quote import SoldProduct
    SoldProduct.__table__.drop(db.engine)
    # db.drop_all()
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


def get_form(heads):
    form = {}
    for head in heads:
        try:
            form[head] = request.form[head]
        except KeyError:
            form[head] = ""

    return form


days = {
    "0": "Lunes", "1": "Martes",
    "2": "Miercoles", "3": "Jueves",
    "4": "Viernes", "5": "Sábado",
    "6": "Domingo"
}
months = {
    "01": "Enero", "02": "Febrero",
    "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio",
    "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre",
    "11": "Noviembre", "12": "Diciembre"
}


def format_date(date):
    str_date = date.strftime("%d/%m/%Y")
    date_parts = str_date.split("/")

    week_day = date.weekday()
    day = days[str(week_day)]
    day_num = date_parts[0]

    month = date_parts[1]
    month = months[month]
    year = date_parts[2]

    return f"{day} {day_num} de {month} del {year}"


def obj_as_dict(obj_tuple):
    obj_dict = {}
    for key in obj_tuple:
        obj_dict[key] = obj_tuple[key]

    return obj_dict