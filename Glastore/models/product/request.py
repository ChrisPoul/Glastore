from flask import request
from Glastore.views import get_form
from . import Product, product_heads


class ProductRequest:

    def __init__(self, product):
        self.product = product
        self.quote = product.quote
        self.error = None

    def add(self):
        error = self.validate()
        if not error:
            self.product.add()

        return error


    def update(self):
        self.update_attributes()
        self.validate()
        self.update_total()
        if self.error is None:
            self.product.update()

        return self.error

    def validate(self):
        self.validate_attributes()
        self.validate_unit_price()

        return self.error

    def validate_attributes(self):
        for head in product_heads:
            value = getattr(self.product, head)
            if value == "":
                self.error = "No se pueden dejar campos en blanco"
                return self.error

    def validate_unit_price(self):
        if not self.product.unit_price:
            self.product.unit_price = 0
        try:
            float(self.product.unit_price)
        except ValueError:
            self.error = "Numero invalido"
            self.product.unit_price = 0
        
        return self.error

    def update_attributes(self):
        attributes = [
            "name",
            "material",
            "acabado",
            "cristal",
            "unit_price",
            "medidas",
            "cantidad"
        ]
        for attribute in attributes:
            self.update_attribute(attribute)

    def update_attribute(self, attribute):
        try:
            request_value = request.form[self.product.unique_keys[attribute]]
            setattr(self.product, attribute, request_value)
        except KeyError:
            pass

    def update_total(self):
        cantidad = float(self.product.cantidad)
        unit_price = float(self.product.unit_price)
        self.product.total = cantidad * unit_price
