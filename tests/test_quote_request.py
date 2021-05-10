from .setup import MyTest
from Glastore.models.quote import Quote
from Glastore.models.customer import Customer
from Glastore.models.product import Product


class QuoteTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.quote = Quote.new(1)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()
        self.product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        self.product.add()