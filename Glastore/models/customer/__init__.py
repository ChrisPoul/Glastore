from sqlalchemy import (
    Column, Integer, String
)
from Glastore.models import db, MyModel

customer_heads = {
    "name": "Nombre del Cliente",
    "email": "Correo electrónico",
    "phone": "Número de teléfono",
    "address": "Dirección"
}


class Customer(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=True, unique=True)
    phone = Column(String(15), nullable=False, unique=True)
    address = Column(String(150), nullable=True, unique=True)
    quotes = db.relationship(
        'Quote', backref='author', lazy=True,
        cascade='all, delete-orphan'
    )
    request_heads = customer_heads

    def get(id):
        return Customer.query.get(id)

    def search(search_term):
        customer = Customer.query.filter_by(name=search_term).first()
        if not customer:
            customer = Customer.query.filter_by(phone=search_term).first()
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
