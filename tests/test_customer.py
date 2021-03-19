from .setup import MyTest
from Glastore.models import Customer, db, repeated_value_msg


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


class CustomersView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/customer/customers'
        )
        self.assertEqual(response.status_code, 200)

    def test_customers(self):
        make_test_customer("Test")
        make_test_customer("Test second")
        response = self.client.get(
            '/customer/customers'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Test second', response.data)


class AddCustomer(MyTest):

    def test_add(self):
        customer = make_test_customer()
        assert customer in db.session

    def test_invalid_name(self):
        customer, error = make_test_customer("1nval1d nam3")
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
            address="Fake address"
        )
        response = self.client.post(
            '/customer/add',
            data=data
        )
        self.assertRedirects(response, '/customer/customers')


class UpdateCustomer(MyTest):

    def test_update(self):
        customer = make_test_customer()
        customer.name = "Test second"
        error = customer.update()
        self.assertEqual(customer.name, "Test second")
        assert error is None

    def test_repeated_name(self):
        customer = make_test_customer()
        make_test_customer("Test second")
        customer.name = "Test second"
        error = customer.update()

        assert error == repeated_value_msg
        assert customer.name == "Test"

    def test_invalid_name(self):
        customer = make_test_customer()
        customer.name = "Test2"
        error = customer.update()
        self.assertEqual(error, customer.invalid_name_msg)

    def test_invalid_email(self):
        customer = make_test_customer()
        customer.email = "test.email.com"
        error = customer.update()
        assert error == customer.invalid_email_msg


class UpdateCustomerView(MyTest):

    def test_view(self):
        make_test_customer()
        response = self.client.get(
            '/customer/update/1'
        )
        self.assertIn(b'Test', response.data)

    def test_update(self):
        customer = make_test_customer()
        data = dict(
            name="Changed name"
        )
        response = self.client.post(
            '/customer/update/1',
            data=data
        )
        self.assertRedirects(response, '/customer/customers')
        self.assertEqual(customer.name, "Changed name")


class DeleteCustomer(MyTest):

    def test_delete(self):
        customer = make_test_customer()
        assert customer in db.session
        customer.delete()
        assert customer not in db.session


class DeleteCustomerView(MyTest):

    def test_delete(self):
        customer = make_test_customer()
        response = self.client.post(
            '/customer/delete/1'
        )
        self.assertRedirects(response, '/customer/customers')
        assert customer not in db.session


class GetCustomer(MyTest):

    def test_get(self):
        customer = make_test_customer()
        assert Customer.get("Test") == customer
        assert Customer.get("Testing") is None

    def test_with_id(self):
        customer = make_test_customer()
        assert Customer.get(1) == customer

    def test_with_email(self):
        customer = make_test_customer()
        customer_search = Customer.get("Test@email.com")
        assert customer_search == customer

    def test_with_address(self):
        customer = make_test_customer()
        customer_search = Customer.get("Fake address of Test")
        assert customer_search == customer


class GetCustomers(MyTest):

    def test_get_all(self):
        customer = make_test_customer()
        customer2 = make_test_customer("Test second")
        customer2.add()
        assert Customer.get_all() == [customer, customer2]
