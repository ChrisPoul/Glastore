from .setup_tests import MyTest
from Glastore.models import Customer, db


class AddCustomer(MyTest):

    def test_add(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        assert customer in db.session

    def test_invalid_name(self):
        customer = Customer(
            name="nam3 w1th numb3rs"
        )
        error = customer.add()
        assert error == "El nombre del cliente no puede llevar numeros, solo letras"

    def test_invalid_email(self):
        customer = Customer(
            name="Test",
            email="test.email.com"
        )
        error = customer.add()
        assert error == "El correo que introdujiste es invalido"

    def test_empty_emial(self):
        customer = Customer(
            name="Test",
            address="A fake address"
        )
        customer.add()
        assert customer in db.session

    def test_empty_address(self):
        customer = Customer(
            name="Test",
            email="chris@email.com"
        )
        customer.add()
        assert customer in db.session


class RemoveCustomer(db.Model):

    def test_remove(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        assert customer in db.session
        customer.remove()
        assert customer not in db.session
