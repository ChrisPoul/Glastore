from flask import request
from .validation import ProductValidation


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
        self.error = self.validation.validate()

        return self.error

    @property
    def validation(self):
        return ProductValidation(self.product)

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
