from Glastore.views import get_form
from . import customer_heads

repeated_value_error = "Ese valor no está disponible, intenta usar otra cosa"


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
                error = repeated_value_error

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
            self.error = repeated_value_error

        return self.error

    def update_attributes(self):
        form = get_form(customer_heads)
        for attribute in customer_heads:
            setattr(self.customer, attribute, form[attribute])

    def validate(self):
        self.error = None
        self.check_for_emtpy_values()
        self.validate_name()
        self.validate_email()
        self.validate_phone()

        return self.error

    def check_for_emtpy_values(self):
        for head in customer_heads:
            attribute = getattr(self.customer, head)
            if attribute == "":
                self.error = "No se pueden dejar campos en blanco"
                return self.error

    def validate_name(self):
        invalid_name_msg = "El nombre del cliente no puede llevar numeros, solo letras"
        nums = "1234567890"
        if not self.error:
            for num in nums:
                if num in self.customer.name:
                    self.error = invalid_name_msg
                    break

    def validate_email(self):
        invalid_email_msg = "El correo que introdujo es invalido"
        if not self.error:
            if "@" not in self.customer.email:
                self.error = invalid_email_msg

    def validate_phone(self):
        invalid_phone_msg = "El teléfono que puso es invalido"
        nums = "1234567890 "
        if not self.error:
            for char in self.customer.phone:
                if char not in nums:
                    self.error = invalid_phone_msg
                    break