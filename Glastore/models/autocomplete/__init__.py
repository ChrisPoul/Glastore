from Glastore.models.customer import Customer, customer_heads
from Glastore.models.product import Product


class Autocomplete:

    @property
    def customer(self):
        return CustomerAutocomplete()

    @property
    def product(self):
        return ProductAutocomplete()


class CustomerAutocomplete:

    def __init__(self):
        self.customers = Customer.get_all()
        self.heads = customer_heads
        self.data = self.get_empty_data()
        self.add_data()
        self.names = self.data["name"]
        self.emails = self.data["email"]
        self.phones = self.data["phone"]
        self.addresses = self.data["address"]

    @property
    def search_bar(self):
        data = []
        for key in self.data:
            for value in self.data[key]:
                data.append(value)

        return data

    def get_empty_data(self):
        data = {}
        for head in self.heads:
            data[head] = []

        return data

    def add_data(self):
        self.data = self.get_empty_data()
        for customer in self.customers:
            self.add_values(customer)
        
        return self.data

    def add_values(self, customer):
        for head in self.heads:
            value = getattr(customer, head)
            self.data[head].append(value)

class ProductAutocomplete:

    def __init__(self):
        self.products = Product.get_all()
        self.heads = [
            "name",
            "material",
            "acabado",
            "cristal"
        ]
        self.data = self.get_empty_data()
        self.add_data()

    def add_data(self):
        for product in self.products:
            self.add_values(product)

    def get_empty_data(self):
        data = {}
        for head in self.heads:
            data[head] = []

        return data

    def add_values(self, product):
        for head in self.heads:
            value = getattr(product, head)
            if value not in set(self.data[head]):
                self.data[head].append(value)