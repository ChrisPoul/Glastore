import click
import base64
from io import BytesIO
from flask import request
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column

db = SQLAlchemy()
repeated_value_msg = "Introdujo un valor que ya está en uso"


class MyModel:

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def delete(self):
        delete_from_db(self)

    def update(self):
        commit_to_db()


def init_db():
    # from .user import User
    # User.__table__.drop(db.engine)
    db.drop_all()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized Database')


def commit_to_db():
    try:
        db.session.commit()
        print("commited to db")
    except IntegrityError:
        db.session.rollback()
        raise ValueError from None


def add_to_db(item):
    db.session.add(item)
    commit_to_db()


def delete_from_db(item):
    db.session.delete(item)
    db.session.commit()


def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

# column = Column('orientacion', String(100), nullable=True, default=1)
# add_column(d.engine, "window", column)


def save_to_temporary_buffer(figure):
        buffer = BytesIO()
        figure.savefig(buffer, format="png")

        return buffer

def get_temporary_uri(figure):
    temporary_buffer = save_to_temporary_buffer(figure)
    data_in_base64 = base64.b64encode(temporary_buffer.getbuffer())
    data = data_in_base64.decode("ascii")
    data_uri = 'data:image/png;base64,{}'.format(data)
    
    return data_uri


days = {
    "0": "Lunes",
    "1": "Martes",
    "2": "Miércoles",
    "3": "Jueves",
    "4": "Viernes",
    "5": "Sábado",
    "6": "Domingo"
}
months = {
    "01": "Enero",
    "02": "Febrero",
    "03": "Marzo",
    "04": "Abril",
    "05": "Mayo",
    "06": "Junio",
    "07": "Julio",
    "08": "Agosto",
    "09": "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
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


def format_price(price, iva=None):
    price = float(price)
    if iva:
        price = price * iva
    price = round(price, 2)
    price = str(price)
    price_int, price_dec = price.split(".")
    price_int = add_comma_separators_to_num(price_int)
    price_dec = format_decimal_of_price(price_dec)
    formated_price = f"${price_int}.{price_dec}"

    return formated_price


def add_comma_separators_to_num(num):
    num = str(num)
    formated_num = ""
    for i, digit in enumerate(num[::-1], start=1):
        formated_num += digit
        if i % 3 == 0:
            formated_num += ","
    formated_num = formated_num[::-1]

    return formated_num


def format_decimal_of_price(decimal):
    if len(decimal) == 1:
        decimal += "0"
    return decimal
