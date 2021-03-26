from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey, Float, String
)
from flask import request
from Glastore.models import (
    db, add_to_db, commit_to_db, get_form
)
from Glastore.models.product import Product


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
    def products(self):
        products = [sold_product.product for sold_product in self.sold_products]
        products = set(products)
        return products

    @property
    def total(self):
        total = 0
        return total

    @property
    def new_product(self):
        if not self.form:
            self.form = get_form(self.product_keys)
        new_product = Product(
            name=self.form['name'],
            material=self.form['material'],
            cristal=self.form['cristal'],
            unit_price=0
        )
        return new_product

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

    def add_product(self, product):
        sold_product = SoldProduct(
            quote_id=self.id,
            product_id=product.id
        )
        error = product.add()
        if not error:
            sold_product.add()
        self.form = {
            "name": "",
            "material": "",
            "cristal": "",
            "medidas": "",
            "unit_price": 0
        }

    def update_products(self):
        for sold_product in self.sold_products:
            sold_product.edit_on_submit()

    def handle_submit(self):
        try:
            product = Product.get(request.form['name'])
        except KeyError:
            product = None
        if product:
            if product in set(self.products):
                new_product = Product(
                    name=product.name,
                    material=product.material,
                    cristal=product.cristal,
                    unit_price=product.unit_price
                )
                new_product.add()
                self.add_product(new_product)
            else:
                self.add_product(product)
        else:
            product = self.new_product
            self.add_product(product)
        self.update_products()


class SoldProduct(db.Model):
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey('quote.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    medidas = Column(String(50), nullable=False, unique=False, default="")
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
            name=f"name{self.id}",
            material=f"material{self.id}",
            cristal=f"cristal{self.id}",
            medidas=f"medidas{self.id}",
            cantidad=f"cantidad{self.id}",
            unit_price=f"unit_price{self.id}"
        )

        return unique_value_keys

    def edit_on_submit(self):
        self.edit_medidas_on_submit()
        self.edit_product_on_submit()
        self.edit_cantidad_on_submit()
        self.update_total()

    def edit_medidas_on_submit(self):
        try:
            self.medidas = request.form[self.unique_keys["medidas"]]
        except KeyError:
            pass

    def edit_product_on_submit(self):
        product = self.product
        previous_name = self.product.name
        try:
            product.name = request.form[self.unique_keys["name"]]
        except KeyError:
            pass
        try:
            product.material = request.form[self.unique_keys["material"]]
        except KeyError:
            pass
        try:
            product.cristal = request.form[self.unique_keys["cristal"]]
        except KeyError:
            pass
        try:
            product.unit_price = request.form[self.unique_keys["unit_price"]]
        except KeyError:
            pass
        error = product.update()
        if error:
            product.name = previous_name
            self.quote.error = error

    def edit_cantidad_on_submit(self):
        try:
            self.cantidad = request.form[self.unique_keys["cantidad"]]
        except KeyError:
            pass

    def update_total(self):
        cantidad = float(self.cantidad)
        self.total = cantidad * self.product.unit_price
