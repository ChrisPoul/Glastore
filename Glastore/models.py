import click
from flask import request
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String, Text,
    PickleType, ForeignKey
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


class Window(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True, unique=False, default="")
    material = Column(String(100), nullable=True, unique=False, default="")
    color = Column(String(100), nullable=True, unique=False, default="")
    cristal = Column(String(100), nullable=True, unique=False, default="")
    acabado = Column(String(100), nullable=True, unique=False, default="")
    modelo = Column(String(100), nullable=True, unique=False, default="")
    herrajes = Column(PickleType, nullable=False, unique=False, default=[])
    sellado = Column(String(100), nullable=True, unique=False, default="")

    def __repr__(self):
        return self.__dict__

    def add(self):
        error = add_to_db(self)
        return error

    def update(self, form=None):
        if form:
            self.name = form["name"]
            self.description = form["description"]
            self.material = form["material"]
            self.color = form["color"]
            self.cristal = form["cristal"]
            self.acabado = form["acabado"]
            self.modelo = form["modelo"]
            self.sellado = form["sellado"]
        error = commit_to_db()

        return error

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def new(name):
        window = Window(name=name)
        error = window.add()
        if error:
            return window, error

        return window

    def get(search_term):
        window = Window.query.get(search_term)
        if not window:
            window = Window.query.filter_by(name=search_term).first()

        return window

    def get_all(search_term=None):
        if not search_term:
            windows = Window.query.all()
        else:
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

        return windows


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    products = Column(PickleType, nullable=False, unique=False, default={})
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
    def totals(self):
        totals = {}
        for id in self.products:
            totals[id] = self.products[id]

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
