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
        assert error == "El correo que introdujo es invalido"

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

    def test_two_empty_customers(self):
        customer = Customer(
            name="Test"
        )
        customer.add()
        customer2 = Customer(
            name="Test second"
        )
        customer2.add()
        assert customer in db.session
        assert customer2 in db.session


class DeleteCustomer(MyTest):

    def test_delete(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        assert customer in db.session
        customer.delete()
        assert customer not in db.session


class GetCustomer(MyTest):

    def test_get(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        assert Customer.get("Test") == customer
        assert Customer.get("Testing") is None

    def test_with_id(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        assert Customer.get(1) == customer

    def test_with_email(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        customer_search = Customer.get("test@email.com")
        assert customer_search == customer

    def test_with_address(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        customer_search = Customer.get("Fake address Apt. 12")
        assert customer_search == customer

    def test_with_cotizacion(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12",
            cotizacion="G20010"
        )
        customer.add()
        customer_search = Customer.get("G20010")
        assert customer_search == customer


class UpdateCustomer(MyTest):

    def test_update(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        customer.name = "Testsecond"
        customer.update()

        customer = Customer.get("Testsecond")
        assert customer

    def test_repeated_name(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        customer2 = Customer(
            name="Testsecond",
            email="test2@email.com",
            address="Fake address Apt. 10"
        )
        customer2.add()

        customer.name = "Testsecond"
        error = customer.update()
        assert error == "Introdujo un valor que ya está en uso"
        customer = Customer.get("test@email.com")
        assert customer.name == "Test"

    def test_invalid_name(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        customer.name = "Test2"
        error = customer.update()
        assert error == "El nombre del cliente no puede llevar numeros, solo letras"

    def test_invalid_email(self):
        customer = Customer(
            name="Test",
            email="test@email.com"
        )
        customer.add()
        customer.email = "test.email.com"
        error = customer.update()
        assert error == "El correo que introdujo es invalido"
