from flask import request


class ProductRequest:

    def __init__(self, product):
        self.product = product
        self.quote = product.quote

    def update(self):
        previous_name = self.product.name
        self.update_attributes()
        self.quote.error = self.product.update()
        if self.quote.error:
            self.product.name = previous_name

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
        self.product.update_total()

    def update_attribute(self, attribute):
        try:
            request_value = request.form[self.product.unique_keys[attribute]]
            setattr(self.product, attribute, request_value)
        except KeyError:
            pass