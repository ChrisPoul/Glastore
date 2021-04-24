from sqlalchemy import (
    Column, Integer, String
)
from Glastore.models import db, add_to_db, commit_to_db

customer_heads = {
    "name": "Nombre del Cliente",
    "email": "Correo electrónico",
    "address": "Dirección"
}


class Customer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    address = Column(String(150), nullable=True, unique=True)
    quotes = db.relationship(
        'Quote', backref='author', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        commit_to_db()

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

    @property
    def request(self):
        from .request import CustomerRequest
        return CustomerRequest(self)
