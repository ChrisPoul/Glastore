from .setup_tests import MyTest
from Glastore.models import add_to_db, Customer
from Glastore import db


class DbTests(MyTest):

    def test_add_to_db(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        add_to_db(customer)
        assert customer in db.session

        customer2 = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        error = add_to_db(customer2)
        assert error == "Ese Valor ya está en uso"
