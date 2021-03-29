from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey
)
from flask import request
from Glastore.models import (
    db, add_to_db, commit_to_db, get_form
)
from Glastore.models.product import Product
from Glastore.models.sold_product import SoldProduct

empty_form = {
    "name": "",
    "material": "",
    "cristal": "",
    "medidas": "",
    "unit_price": 0
}


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    sold_products = db.relationship(
        'SoldProduct', backref='quote', lazy=True,
        cascade='all, delete-orphan'
    )
    error = None
    form = None
    product_keys = [
        "name",
        "material",
        "cristal",
        "medidas",
        "unit_price"
    ]

    def __repr__(self):
        return self.__dict__

    def add(self):
        self.error = add_to_db(self)
        return self.error

    def update(self):
        if not self.error:
            self.error = commit_to_db()
        return self.error

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
        for sold_product in self.sold_products:
            total += sold_product.total
        return total

    @property
    def products(self):
        products = [sold_product.product for sold_product in self.sold_products]
        return products

    @property
    def new_product(self):
        if not self.form:
            self.form = self.get_form()
        new_product = Product(
            name=self.form['name'],
            material=self.form['material'],
            cristal=self.form['cristal'],
            unit_price=0
        )
        return new_product

    def handle_submit(self):
        self.add_product_on_submit()
        self.update_sold_products_on_submit()
        self.form = empty_form

    def add_product_on_submit(self):
        product = self.get_product_on_submit()
        if product:
            self.add_existing_product(product)
        else:
            self.add_new_product_on_submit()

    def add_existing_product(self, product):
        if product in set(self.products):
            self.add_new_duplicate_product(product)
        else:
            self.add_product(product)

    def add_new_duplicate_product(self, product):
        new_product = Product(
            name=product.name,
            material=product.material,
            cristal=product.cristal,
            unit_price=product.unit_price
        )
        new_product.add()
        self.add_product(new_product)

    def add_new_product_on_submit(self):
        product = self.new_product
        self.error = product.add()
        if not self.error:
            self.add_product(product)

    def add_product(self, product):
        sold_product = SoldProduct(
            quote_id=self.id,
            product_id=product.id
        )
        sold_product.add()

    def get_product_on_submit(self):
        try:
            product = Product.get(request.form['name'])
        except KeyError:
            product = None

        return product

    def get_form(self):
        return get_form(self.product_keys)

    def update_sold_products_on_submit(self):
        for sold_product in self.sold_products:
            sold_product.update_on_submit()

    @property
    def autocomplete_data(self):
        autocomplete = {
            "names": [],
            "materials": [],
            "cristals": []
        }
        for product in Product.get_all():
            if product.name not in set(autocomplete["names"]):
                autocomplete["names"].append(product.name)
            if product.material not in set(autocomplete["materials"]):
                autocomplete["materials"].append(product.material)
            if product.cristal not in set(autocomplete["cristals"]):
                autocomplete["cristals"].append(product.cristal)
        return autocomplete
