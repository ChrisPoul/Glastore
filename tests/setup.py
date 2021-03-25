from flask_testing import TestCase
from Glastore.models import db
from Glastore import create_app
from Glastore.models.product import Product
from Glastore.models.quote import Quote
from Glastore.models.customer import Customer


def make_test_customer(name="Test"):
    customer = Customer(
        name=name,
        email=f"{name}@email.com",
        address=f"Fake address of {name}"
    )
    error = customer.add()
    if error:
        return customer, error

    return customer


class MyTest(TestCase):

    def create_app(self):
        test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True
        }
        app = create_app(test_config)

        return app

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()
        self.customer = make_test_customer()
        self.product = Product(
            name="Test Product",
            material="Test Material",
            cristal="Test Cristal",
            medidas="1x1"
        )
        self.product.add()
        self.quote = Quote.new(self.customer.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def request_context(self, url, data):
        with self.client:
            with self.app.test_request_context(url, data=data) as request_context:
                return request_context
