from .setup import MyTest
from Glastore.models import add_to_db, Customer, db


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
        assert error == "Introdujo un valor que ya está en uso"
        assert customer2 not in db.session
