from datetime import datetime
from flask import request
from Glastore.models.product import Product
from Glastore.views import get_form
from .validation import QuoteValidation

empty_form = {
    "name": "",
    "material": "",
    "acabado": "",
    "cristal": "",
    "medidas": "",
    "unit_price": 0
}


class QuoteRequest:

    def __init__(self, quote):
        self.quote = quote
        self.customer = quote.author
        self.products = quote.products
        self.customer.request_heads = [
            "customer_name",
            "email"
        ]
        self.product_keys = {
            "name": "Suministro y colocación de ",
            "material": "en ",
            "acabado": "acabado ", 
            "cristal": "con ",
            "medidas": "Dimenciones"
        }
        self.error = None

    def edit(self):
        self.update_attributes()
        self.validate()
        if not self.error:
            self.quote.update()
            self.add_product()

        return self.error

    def validate(self):
        self.error = self.validation.validate()

        return self.error

    @property
    def validation(self):
        return QuoteValidation(self.quote)

    def update_attributes(self):
        self.update_address()
        self.update_date()
        self.update_customer()
        self.update_products()

    def update_customer(self):
        self.customer.request.update_attributes()

    def update_products(self):
        for product in self.products:
            product.request.update_attributes()

    def update_address(self):
        if not self.quote.address:
            self.quote.address = self.customer.address
        self.attempt_update_address()

        return self.error

    def attempt_update_address(self):
        try:
            self.quote.address = request.form["address"]
        except KeyError:
            pass

    def update_date(self):
        self.quote.date = datetime.now()

    def add_product(self):
        product = self.get_product()
        if product:
            self.quote.add_product(product)
        else:
            self.add_new_product()

    def add_new_product(self):
        product = self.new_product
        error = product.request.add()
        if error:
            self.quote.focused_product_id = 0
        else:
            self.quote.focused_product_id = product.id

    def get_product(self):
        try:
            product = Product.search(request.form['name'])
        except KeyError:
            product = None

        return product

    @property
    def new_product(self):
        form = get_form(empty_form)
        product = Product.search(form["name"])
        if product:
            form = empty_form
        product = self.make_product(form)

        return product

    def make_product(self, form):
        product = Product(
            quote_id=self.quote.id,
            name=form['name'],
            material=form['material'],
            acabado=form['acabado'],
            cristal=form['cristal'],
            unit_price=0
        )

        return product

    def done(self):
        from . import SoldQuote
        sold_quote = SoldQuote(
            quote_id=self.quote.id,
            date=datetime.now(),
            total=self.quote.total
        )
        sold_quote.add()