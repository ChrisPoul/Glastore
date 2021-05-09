from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, String, Float
)
from Glastore.models import db, MyModel
from Glastore.models.product import Product
from Glastore.models.window import Window
from .request import QuoteRequest


class Quote(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    address = Column(String(100), nullable=True, unique=False)
    products = db.relationship(
        'Product', backref='quote', lazy=True,
        cascade='all, delete-orphan'
    )
    sold_quotes = db.relationship(
        'SoldQuote', backref='quote', lazy=True,
        cascade='all, delete-orphan'
    )
    focused_product_id = Column(Integer, nullable=False, default=0)

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
    def total(self):
        total = 0
        for product in self.products:
            total += product.total
        return total

    @property
    def request(self):
        return QuoteRequest(self)

    def add_product(self, product):
        new_product = Product(
            quote_id=self.id,
            name=product.name,
            material=product.material,
            acabado=product.acabado,
            cristal=product.cristal,
            unit_price=product.unit_price
        )
        new_product.add()


class SoldQuote(db.Model):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    total = Column(Float, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__

    def add(self):
        add_to_db(self)

    def update(self):
        commit_to_db()

    def delte(self):
        delete_from_db(self)

    def get(id):
        return SoldQuote.query.get(id)

    def get_all():
        return SoldQuote.query.all()
