from .setup_tests import MyTest
from Glastore.models import Customer, add_to_db
from Glastore import db


class CustomerTests(MyTest):

    def test_add_customer(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        add_to_db(customer)

        assert customer in db.session
