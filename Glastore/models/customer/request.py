from Glastore.models import get_form
from . import Customer, customer_heads


class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer
        self.error = None
    
    def add(self):
        error = self.validate()
        if not error:
            try:
                self.customer.add()
            except ValueError:
                error = "Eso ya está en uso"

        return error

    def update(self):
        self.update_attributes()
        self.validate()
        if not self.error:
            self.attempt_update()

        return self.error

    def attempt_update(self):
        try:
            self.customer.update()
        except ValueError:
            self.error = "Eso ya siusa"

        return self.error

    def update_attributes(self):
        form = get_form(customer_heads)
        for attribute in customer_heads:
            setattr(self.customer, attribute, form[attribute])

    def validate(self):
        self.error = None
        self.check_for_emtpy_values()
        if not self.error:
            self.validate_name()
            self.validate_email()

        return self.error

    def check_for_emtpy_values(self):
        for head in customer_heads:
            attribute = getattr(self.customer, head)
            if attribute == "":
                self.error = "No se pueden dejar campos en blanco"
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