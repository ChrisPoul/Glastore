from datetime import datetime
from flask import request
from Glastore.models.customer import Customer
from Glastore.models.product import Product
from Glastore.views import get_form


class QuoteRequest:

    def __init__(self, quote):
        self.quote = quote
        self.customer = quote.author
        self.products = quote.products
        self.error = None
        self.customer_heads = [
            "name",
            "email"
        ]
        self.product_keys = {
            "name": "Suministro y colocación de ",
            "material": "en ",
            "acabado": "acabado ", 
            "cristal": "con ",
            "medidas": "Dimenciones"
        }

    def add(self):
        pass

    def edit(self):
        self.validate()
        self.update_address()
        self.update_customer()
        self.add_product()
        self.update_products()
        self.update_date()

        return self.error

    def validate(self):
        if self.quote.address == "":
            self.error = "No se pueden dejar campos en blanco"
        
        return self.error

    def update_date(self):
        if not self.error:
            self.quote.date = datetime.now()
            self.quote.update()

    def update_address(self):
        if not self.quote.address:
            self.quote.address = self.customer.address
        if not self.error:
            self.attempt_update_address()

        return self.error

    def attempt_update_address(self):
        try:
            self.quote.address = request.form["address"]
        except KeyError:
            pass
        self.quote.update()

    def update_customer(self):
        self.update_customer_attributes()
        error = self.customer.request.validate()
        if not error:
            self.error = self.customer.request.attempt_update()
        else:
            self.error = error

        return self.error

    def update_customer_attributes(self):
        for attribute in self.customer_heads:
            self.update_customer_attribute(attribute)

    def update_customer_attribute(self, attribute):
        if attribute == "name":
            head = "customer_name"
        else:
            head = attribute
        self.attempt_update_customer_attribute(attribute, head)
    
    def attempt_update_customer_attribute(self, attribute, head):
        try:
            value = request.form[head]
            setattr(self.customer, attribute, value)
        except KeyError:
            pass

    def add_product(self):
        error = None
        product = self.get_product()
        if product:
            self.quote.add_product(product)
        else:
            error = self.add_new_product()

        return error

    def add_new_product(self):
        product = self.new_product
        error = product.request.add()
        if error:
            self.quote.focused_product_id = 0
        else:
            self.quote.focused_product_id = product.id

        return error

    def get_product(self):
        try:
            product = Product.search(request.form['name'])
        except KeyError:
            product = None

        return product

    def update_products(self):
        for product in self.products:
            error = product.request.update()
            if error:
                self.error = error
                return error

    @property
    def new_product(self):
        form = get_form(empty_form)
        product = Product.search(form["name"])
        if product:
            form = empty_form
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

    @property
    def autocomplete_data(self):
        return get_autocomplete_data()


def get_autocomplete_data():
    autocomplete = {
        "names": [],
        "materials": [],
        "acabados": [],
        "cristals": []
    }
    for product in Product.get_all():
        if product.name not in set(autocomplete["names"]):
            autocomplete["names"].append(product.name)
        if product.material not in set(autocomplete["materials"]):
            autocomplete["materials"].append(product.material)
        if product.cristal not in set(autocomplete["cristals"]):
            autocomplete["cristals"].append(product.cristal)
        if product.acabado not in set(autocomplete["acabados"]):
            autocomplete["acabados"].append(product.acabado)
    return autocomplete


empty_form = {
    "name": "",
    "material": "",
    "acabado": "",
    "cristal": "",
    "medidas": "",
    "unit_price": 0
}
