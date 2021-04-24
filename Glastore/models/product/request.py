from flask import request


class ProductRequest:

    def __init__(self, product):
        self.product = product
        self.quote = product.quote
        self.error = None

    def update(self):
        self.update_attributes()
        self.validate()
        self.update_total()
        if self.error is None:
            self.product.update()

        return self.error

    def validate(self):
        self.validate_fields()
        self.validate_price()

        return self.error

    def validate_fields(self):
        if self.product.name == "" or self.product.material == "" or self.product.cristal == "" or self.product.acabado == "":
            self.error = "No se pueden dejar campos en blanco"

    def validate_price(self):
        if self.product.unit_price:
            try:
                float(self.product.unit_price)
            except ValueError:
                self.error = "Numero invalido"
                self.product.unit_price = 0
        else:
            self.product.unit_price = 0

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
        self.total = cantidad * unit_price
