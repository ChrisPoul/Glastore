import click
from datetime import datetime
from flask import request
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String,
    PickleType, ForeignKey, DateTime
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
    quotes = db.relationship(
        'Quote', backref='author', lazy=True,
        cascade='all, delete-orphan'
    )

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

    def update(self, form=None):
        if form:
            self.name = form['name']
            self.email = form['email']
            self.address = form['address']
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

        return customer

    def get_all():
        return Customer.query.all()


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    material = Column(String(100), nullable=True, unique=False, default="")
    cristal = Column(String(100), nullable=True, unique=False, default="")
    medidas = Column(String(50), nullable=True, unique=False, default="")
    acabado = Column(String(100), nullable=True, unique=False, default="")

    def __repr__(self):
        return self.__dict__

    def add(self):
        error = add_to_db(self)
        return error

    def update(self, form=None):
        if form:
            self.name = form["name"]
            self.material = form["material"]
            self.cristal = form["cristal"]
            self.medidas = form["medidas"]
        error = commit_to_db()

        return error

    def edit_in_quote(self, form):
        try:
            self.material = form[f"{self.id}material"]
        except KeyError:
            pass
        try:
            self.cristal = form[f"{self.id}cristal"]
        except KeyError:
            pass
        try:
            self.medidas = form[f"{self.id}medidas"]
        except KeyError:
            pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def new(name):
        product = Product(name=name)
        error = product.add()
        if error:
            return product, error

        return product

    def get(search_term):
        product = Product.query.get(search_term)
        if not product:
            product = Product.query.filter_by(name=search_term).first()

        return product

    def get_all(search_term=None):
        if not search_term:
            products = Product.query.all()
        else:
            products = Product.query.filter_by(material=search_term).all()
            if not products:
                products = Product.query.filter_by(cristal=search_term).all()

        return products


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    cantidades = Column(PickleType, nullable=False, unique=False, default={})
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return self.__dict__

    @property
    def folio(self):
        id = str(self.id)
        folio = "G"
        num_of_zeros = 5 - len(id)
        for _ in range(num_of_zeros):
            folio += "0"
        folio += id

        return folio

    @property
    def products(self):
        products = []
        for id in self.cantidades:
            product = Product.get(id)
            product.edit_in_quote(request.form)
            products.append(product)

        return products

    @property
    def totals(self):
        totals = {}
        for id in self.cantidades:
            totals[id] = self.cantidades[id]

        return totals

    @property
    def total(self):
        total = 0
        for id in self.totals:
            total += self.totals[id]

        return total

    def add(self):
        error = add_to_db(self)
        return error

    def update(self):
        error = commit_to_db()
        return error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def new(customer_id=1):
        quote = Quote(customer_id=customer_id)
        quote.add()

        return quote

    def get(id):
        return Quote.query.get(id)

    def get_all(customer_id=None):
        if not customer_id:
            quotes = Quote.query.all()
        else:
            quotes = Quote.query.filter_by(customer_id=customer_id).all()

        return quotes

    def add_product(self, product):
        cantidades = obj_as_dict(self.cantidades)
        cantidades[product.id] = 0
        self.cantidades = cantidades
        self.update()


def init_db():
    # Product.__table__.drop(db.engine)
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
