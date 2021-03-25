from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, Float
)
from flask import request
from Glastore.models import db, add_to_db, commit_to_db, get_form
from Glastore.models.product import Product


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    sold_products = db.relationship(
        'SoldProduct', backref='quote', lazy=True,
        cascade='all, delete-orphan'
    )

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
        products = [sold_product.product for sold_product in self.sold_products]
        return products

    @property
    def total(self):
        total = 0
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

    @property
    def new_product(self):
        product_keys = [
            "name",
            "material",
            "cristal",
            "medidas"
        ]
        form = get_form(product_keys)
        new_product = Product(
            name=form['name'],
            material=form['material'],
            cristal=form['cristal'],
            medidas=form['medidas']
        )
        return new_product

    def add_product(self, product):
        if product not in self.products:
            sold_product = SoldProduct(
                quote_id=self.id,
                product_id=product.id
            )
            sold_product.add()

    def update_products(self):
        for sold_product in self.sold_products:
            # sold_product.update_cantidades()
            sold_product.edit_on_submit()

    def handle_submit(self):
        try:
            product = Product.get(request.form['name'])
        except KeyError:
            product = None
        if product:
            self.add_product(product)
        self.update_products()


class SoldProduct(db.Model):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    total = Column(Float, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__

    def add(self):
        self.cantidad = 0
        error = add_to_db(self)
        return error

    def update(self):
        error = commit_to_db()
        return error

    def get(id):
        return SoldProduct.query.get(id)

    @property
    def unique_keys(self):
        unique_value_keys = dict(
            material=f"material{self.id}",
            cristal=f"cristal{self.id}",
            medidas=f"medidas{self.id}",
            cantidad=f"cantidad{self.id}"
        )

        return unique_value_keys

    def edit_on_submit(self):
        self.edit_product_on_submit()
        self.edit_cantidad_on_submit()
        self.update_total()

    def edit_product_on_submit(self):
        product = self.product
        try:
            product.material = request.form[self.unique_keys["material"]]
        except KeyError:
            pass
        try:
            product.cristal = request.form[self.unique_keys["cristal"]]
        except KeyError:
            pass
        try:
            product.medidas = request.form[self.unique_keys["medidas"]]
        except KeyError:
            pass

    def edit_cantidad_on_submit(self):
        try:
            self.cantidad = request.form[self.unique_keys["cantidad"]]
        except KeyError:
            pass

    def update_total(self):
        cantidad = float(self.cantidad)
        self.total = cantidad * self.product.unit_price
