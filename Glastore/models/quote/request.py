from flask import request
from Glastore.models.customer import Customer
from Glastore.models.product import Product
from Glastore.models import get_form


class QuoteRequest:

    def __init__(self, quote):
        self.quote = quote
        self.customer = quote.author
        self.products = quote.products
        self.error = None
        self.customer_heads = {
            "name": "Cliente",
            "email": "Email",
        }
        self.product_keys = {
            "name": "Suministro y colocación de ",
            "material": "en ",
            "acabado": "acabado ", 
            "cristal": "con ",
            "medidas": "Dimenciones"
        }

    def handle(self):
        self.update_address()
        self.update_customer()
        self.add_product()
        self.update_products()

        return self.error

    def update_address(self):
        if self.quote.address == "":
            self.error = "No se pueden dejar campos en blanco"
        if not self.error:
            self.quote.address = request.form["address"]
            self.quote.update()

    def update_customer(self):
        self.update_customer_attributes()
        error = self.customer.request.validate()
        if not error:
            self.error = self.customer.request.attempt_update()
        else:
            self.error = error

    def update_customer_attributes(self):
        for attribute in self.customer_heads:
            self.update_customer_attribute(attribute)

    def update_customer_attribute(self, attribute):
        if attribute == "name":
            head = "customer_name"
        else:
            head = attribute
        setattr(self.customer, attribute, request.form[head])

    def add_product(self):
        product = self.get_product()
        if product:
            self.quote.add_product(product)
        else:
            self.add_new_product()

    def add_new_product(self):
        product = self.new_product
        error = product.request.validate()
        if error:
            self.quote.focused_product_id = 0
        else:
            product.add()
            self.quote.focused_product_id = product.id

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
                break

    @property
    def new_product(self):
        form = self.product_form
        new_product = Product(
            quote_id=self.quote.id,
            name=form['name'],
            material=form['material'],
            acabado=form['acabado'],
            cristal=form['cristal'],
            unit_price=0
        )

        return new_product

    @property
    def product_form(self):
        form = get_form(self.product_keys)
        product = Product.search(form["name"])
        if product:
            form = {
                "name": "",
                "material": "",
                "acabado": "",
                "cristal": "",
                "medidas": "",
                "unit_price": 0
            }

        return form

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
