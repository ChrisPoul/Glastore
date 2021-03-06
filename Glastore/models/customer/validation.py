from . import Customer, customer_heads


class CustomerValidation:

    def __init__(self, customer):
        self.customer = customer
        self.error = None

    def validate(self):
        self.check_for_emtpy_values()
        if not self.error:
            self.check_for_repeated_values()
        if not self.error:
            self.validate_name()
        if not self.error:
            self.validate_email()
        if not self.error:
            self.validate_phone()

        return self.error

    def check_for_emtpy_values(self):
        for head in customer_heads:
            value = getattr(self.customer, head)
            if value == "":
                self.error = "No se pueden dejar campos en blanco"
                return self.error
        
        return self.error

    def check_for_repeated_values(self):
        for head in customer_heads:
            value = getattr(self.customer, head)
            self.check_for_repeated_value(value)
            if self.error:
                return self.error

        return self.error

    def check_for_repeated_value(self, value):
        repeated_value_error = "Ese valor no está disponible, intenta usar otra cosa"
        customer = Customer.search(value)
        if customer and self.customer is not customer:
            self.error = repeated_value_error
            return self.error

    def validate_name(self):
        invalid_name_msg = "El nombre del cliente no puede llevar numeros, solo letras"
        nums = "1234567890"
        for num in nums:
            if num in self.customer.name:
                self.error = invalid_name_msg
                return self.error

        return self.error

    def validate_email(self):
        invalid_email_msg = "El correo que introdujo es invalido"
        if "@" not in self.customer.email:
            self.error = invalid_email_msg

        return self.error

    def validate_phone(self):
        invalid_phone_msg = "El teléfono que puso es invalido"
        nums = "+1234567890 "
        for char in self.customer.phone:
            if char not in nums:
                self.error = invalid_phone_msg
                return self.error

        return self.error