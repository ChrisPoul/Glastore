from flask import url_for
from .setup import MyTest
from Glastore.models import db
from Glastore.models.customer import Customer
from Glastore.models.customer.request import CustomerRequest


class CustomerRequestTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    
class TestAdd(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )

    def test_add(self):
        customer_request = CustomerRequest(self.customer)
        error = customer_request.add()

        self.assertIn(self.customer, db.session)
        self.assertEqual(error, None)       

    def test_repeated_name(self):
        self.customer.add()
        customer = Customer(
            name="Test",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertNotIn(customer, db.session)
        self.assertNotEqual(error, None)


class TestUpdate(CustomerRequestTest):

    def test_update(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="New Name",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertEqual(error, None)
        self.assertEqual(self.customer.name, "New Name")

    def test_repeated_name(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer.add()
        customer_request = CustomerRequest(customer)
        url = url_for('customer.update', customer_id=customer.id)
        data = dict(
            name="Test",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertNotEqual(error, None)
        self.assertNotEqual(customer.name, "Test")

    def test_update_attributes(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="New Name",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, data):
            customer_request.update_attributes()

        self.assertEqual(self.customer.name, "New Name")

    def test_attempt_update(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer.add()
        customer_request = CustomerRequest(customer)
        customer.name = "Test"
        error = customer_request.attempt_update()

        self.assertNotEqual(error, None)
        self.assertNotEqual(customer.name, "Test")


class TestValidate(CustomerRequestTest):

    def test_validate(self):
        customer_request = CustomerRequest(self.customer)
        error = customer_request.validate()

        self.assertEqual(error, None)

    def test_empty_value(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertNotEqual(error, None)

    def test_invalid_name(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="Test2",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertNotEqual(error, None)

    def test_invalid_email(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="Test",
            email="test.email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertNotEqual(error, None)

    def test_invalid_phone(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', customer_id=self.customer.id)
        data = dict(
            name="Test",
            email="test@email.com",
            phone="some text",
            address="Test address"
        )
        with self.request_context(url, data):
            error = customer_request.update()

        self.assertNotEqual(error, None)

