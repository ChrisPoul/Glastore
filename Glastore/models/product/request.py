from flask import request
from Glastore.views import get_form
from . import Product, product_heads


class ProductRequest:

    def __init__(self, product):
        self.product = product
        self.quote = product.quote
        self.product_attributes = [
            "name",
            "material",
            "acabado",
            "cristal",
            "unit_price",
            "medidas",
            "cantidad"
        ]
        self.error = None

    def add(self):
        self.validate()
        if not self.error:
            self.product.add()

        return self.error

    def update(self):
        self.update_attributes()
        self.validate()
        if self.error is None:
            self.update_total()
            self.product.update()

        return self.error

    def validate(self):
        self.check_for_empty_values()
        if not self.error:
            self.validate_unit_price()
        if not self.error:
            self.validate_cantidad()

        return self.error

    def check_for_empty_values(self):
        for head in product_heads:
            value = getattr(self.product, head)
            if value == "":
                self.error = "No se pueden dejar campos en blanco"
                return self.error

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

    def validate_cantidad(self):
        if not self.product.cantidad:
            self.product.cantidad = 0
        try:
            float(self.product.cantidad)
        except ValueError:
            self.error = "Numero invalido"
            self.product.cantidad = 0
        
        return self.error

    def update_attributes(self):
        for attribute in self.product_attributes:
            self.update_attribute(attribute)

    def update_attribute(self, attribute):
        try:
            value = request.form[self.product.unique_keys[attribute]]
            setattr(self.product, attribute, value)
        except KeyError:
            pass

    def update_total(self):
        cantidad = self.product.cantidad
        unit_price = self.product.unit_price
        self.product.total = cantidad * unit_price
