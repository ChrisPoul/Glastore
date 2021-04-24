from flask import request
from Glastore.models.product import Product

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
        self.products = quote.products
        self.error = None

    def handle(self):
        self.add_product()
        self.update_products()
        self.quote.form = empty_form

        return self.error

    def add_product(self):
        product = self.get_product()
        if product:
            self.quote.add_product(product)
        else:
            self.add_new_product()

    def add_new_product(self):
        product = self.quote.new_product
        error = product.request.validate()
        if error:
            self.quote.focused_product_id = 0
        else:
            product.add()
            self.quote.focused_product_id = product.id

    def get_product(self):
        try:
            product = Product.get(request.form['name'])
        except KeyError:
            product = None

        return product

    def update_products(self):
        for product in self.products:
            error = product.request.update()
            if error:
                self.error = error
                break
