from .setup_tests import MyTest
from Glastore.models import Customer, db, repeated_value_msg


class CustomersView(MyTest):

    def test_view(self):
        pass


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
        assert error == customer.invalid_name_msg

    def test_invalid_email(self):
        customer = Customer(
            name="Test",
            email="test.email.com"
        )
        error = customer.add()
        assert error == customer.invalid_email_msg

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


class AddCustomerView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/customer/add'
        )
        self.assertIn(b'Registrar Cliente', response.data)

    def test_add(self):
        data = dict(
            name="Test",
            email="test@email.com",
            address="Fake address",
            cotizacion="G200"
        )
        response = self.client.post(
            '/customer/add',
            data=data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


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
        assert error == repeated_value_msg
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
        assert error == customer.invalid_name_msg

    def test_invalid_email(self):
        customer = Customer(
            name="Test",
            email="test@email.com"
        )
        customer.add()
        customer.email = "test.email.com"
        error = customer.update()
        assert error == customer.invalid_email_msg


class UpdateCustomerView(MyTest):

    def test_view(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address",
            cotizacion="G200"
        )
        customer.add()
        response = self.client.get(
            '/customer/update/1'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'test@email.com', response.data)
        self.assertIn(b'Fake address', response.data)
        self.assertIn(b'G200', response.data)

    def test_update(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        customer.add()
        data = dict(
            cotizacion="G200"
        )
        response = self.client.post(
            '/customer/update/1',
            data=data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


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


class GetCustomers(MyTest):

    def test_get_all(self):
        customer = Customer(
            name="Test"
        )
        customer.add()
        customer2 = Customer(
            name="Test second"
        )
        customer2.add()
        assert Customer.get_all() == [customer, customer2]
