from Glastore.models import get_form
from . import Customer, customer_heads


class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer
    
    def add(self):
        error = self.validate()
        try:
            self.customer.add()
        except ValueError:
            error = "Eso ya está en uso"

        return error

    def update(self):
        form = get_form(customer_heads)
        for attribute in customer_heads:
            setattr(self.customer, attribute, form[attribute])
        error = self.validate()
        try:
            self.customer.update()
        except ValueError:
            error = "Eso ya siusa"

        return error

    def validate(self):
        self.error = None
        self.validate_name()
        self.validate_email()

        return self.error

    def validate_name(self):
        invalid_name_msg = "El nombre del cliente no puede llevar numeros, solo letras"
        if not self.error:
            nums = "1234567890"
            for num in nums:
                if num in self.customer.name:
                    self.error = invalid_name_msg
                    break

    def validate_email(self):
        invalid_email_msg = "El correo que introdujo es invalido"
        if not self.error:
            if "@" not in self.customer.email:
                self.error = invalid_email_msg