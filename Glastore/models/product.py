from sqlalchemy import (
    Column, Integer, String,
    Float
)
from Glastore.models import db, add_to_db, commit_to_db


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    material = Column(String(100), nullable=False, unique=False, default="")
    cristal = Column(String(100), nullable=False, unique=False, default="")
    medidas = Column(String(50), nullable=False, unique=False, default="")
    acabado = Column(String(100), nullable=False, unique=False, default="")
    unit_price = Column(Float, nullable=False, default=0)
    sold_products = db.relationship(
        'SoldProduct', backref='product', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return self.__dict__

    def add(self):
        error = self.validate_price()
        if not error:
            error = add_to_db(self)
        return error

    def update(self, form=None):
        if form:
            self.name = form["name"]
            self.material = form["material"]
            self.cristal = form["cristal"]
            self.medidas = form["medidas"]
            self.unit_price = form["unit_price"]
        error = self.validate_price()
        if not error:
            error = commit_to_db()

        return error

    def validate_price(self):
        error = None
        if self.unit_price:
            try:
                int(self.unit_price)
            except ValueError:
                error = "Numero invalido"
                self.unit_price = 0
        else:
            self.unit_price = 0

        return error

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
