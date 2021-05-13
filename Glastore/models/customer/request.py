from flask import request
from Glastore.views import get_form
from . import customer_heads
from .validation import CustomerValidation


class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer
        self.error = None
    
    def add(self):
        self.validate()
        if not self.error:
            self.customer.add()

        return self.error

    def update(self):
        self.update_attributes()
        self.validate()
        if not self.error:
            self.customer.update()

        return self.error

    def update_attributes(self):
        form = get_form(self.customer.request_heads)
        for attribute, head in zip(customer_heads, self.customer.request_heads):
            setattr(self.customer, attribute, form[head])

    def validate(self):
        self.error = self.validation.validate()

        return self.error

    @property
    def validation(self):
        return CustomerValidation(self.customer)