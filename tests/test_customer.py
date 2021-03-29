from .setup import MyTest, make_test_customer
from Glastore.models import db, repeated_value_msg
from Glastore.models.customer import Customer


class AddCustomer(MyTest):

    def test_add(self):
        customer = make_test_customer("Test second")
        assert customer in db.session

    def test_invalid_name(self):
        customer = Customer(
            name="1inval1d nam3"
        )
        error = customer.add()
        self.assertEqual(error, customer.invalid_name_msg)

    def test_invalid_email(self):
        customer = Customer(
            name="test",
            email="test.email.com"
        )
        error = customer.add()
        self.assertEqual(error, customer.invalid_email_msg)


class AddCustomerView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/customer/add'
        )
        self.assertIn(b'Registrar Cliente', response.data)

    def test_add(self):
        data = dict(
            name="test",
            email="test@email.com",
            address="Fake address"
        )
        response = self.client.post(
            '/customer/add',
            data=data
        )
        self.assertRedirects(response, '/customer/customers')


class UpdateCustomer(MyTest):

    def test_update(self):
        self.customer.name = "Test second"
        error = self.customer.update()
        self.assertEqual(self.customer.name, "Test second")
        assert error is None

    def test_repeated_name(self):
        customer = make_test_customer("Test second")
        customer.name = "Test"
        error = customer.update()

        assert error == repeated_value_msg
        assert customer.name == "Test second"

    def test_invalid_name(self):
        self.customer.name = "Test2"
        error = self.customer.update()
        self.assertEqual(error, self.customer.invalid_name_msg)

    def test_invalid_email(self):
        self.customer.email = "test.email.com"
        error = self.customer.update()
        assert error == self.customer.invalid_email_msg


class UpdateCustomerView(MyTest):

    def test_view(self):
        make_test_customer()
        response = self.client.get(
            '/customer/update/1'
        )
        self.assertIn(b'Test', response.data)

    def test_update(self):
        data = dict(
            name="Changed name"
        )
        response = self.client.post(
            '/customer/update/1',
            data=data
        )
        self.assertRedirects(response, '/customer/customers')
        self.assertEqual(self.customer.name, "Changed name")


class DeleteCustomer(MyTest):

    def test_delete(self):
        assert self.customer in db.session
        self.customer.delete()
        assert self.customer not in db.session


class DeleteCustomerView(MyTest):

    def test_delete(self):
        response = self.client.post(
            '/customer/delete/1'
        )
        self.assertRedirects(response, '/customer/customers')
        assert self.customer not in db.session


class GetCustomer(MyTest):

    def test_get(self):
        assert Customer.get("Test") == self.customer
        assert Customer.get("Testing") is None

    def test_with_id(self):
        assert Customer.get(1) == self.customer

    def test_with_email(self):
        customer_search = Customer.get("Test@email.com")
        assert customer_search == self.customer

    def test_with_address(self):
        customer_search = Customer.get("Fake address of Test")
        assert customer_search == self.customer


class GetCustomers(MyTest):

    def test_get_all(self):
        customer = make_test_customer("Test second")
        customer.add()
        assert Customer.get_all() == [self.customer, customer]


class CustomersView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/customer/customers'
        )
        self.assertEqual(response.status_code, 200)

    def test_customers(self):
        make_test_customer("Test second")
        response = self.client.get(
            '/customer/customers'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Test second', response.data)
