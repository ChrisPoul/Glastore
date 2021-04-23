from Glastore.models import get_form
from . import Customer, customer_heads


class CustomerRequest:

    def __init__(self, customer):
        self.customer = customer
    
    def add(self):
        error = None
        try:
            self.customer.add()
        except ValueError:
            error = "Eso ya está en uso"

        return error

    def update(self):
        form = get_form(customer_heads)
        self.customer.name = form['name']
        self.customer.email = form['email']
        self.customer.address = form['address']
        error = self.customer.update()

        return error