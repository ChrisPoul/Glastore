from . import product_heads


class ProductValidation:

    def __init__(self, product):
        self.product = product
        self.error = None

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
            int(self.product.cantidad)
        except ValueError:
            self.error = "Numero invalido"
            self.product.cantidad = 0
        
        return self.error