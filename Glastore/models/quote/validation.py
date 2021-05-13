

class QuoteValidation:

    def __init__(self, quote):
        self.quote = quote
        self.customer = quote.author
        self.products = quote.products
        self.error = None

    def validate(self):
        self.validate_address()
        if not self.error:
            self.validate_customer()
        if not self.error:
            self.validate_products()
        
        return self.error

    def validate_address(self):
        if self.quote.address == "":
            self.error = "No se pueden dejar campos en blanco"

        return self.error

    def validate_customer(self):
        self.error = self.customer.request.validate()

        return self.error

    def validate_products(self):
        for product in self.products:
            self.error = product.request.validate()
            if self.error:
                return self.error

        return self.error
