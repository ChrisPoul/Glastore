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

    def test_empty_value(self):
        customer = Customer(
            name="",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertNotEqual(error, None)
        self.assertNotIn(customer, db.session)        

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

    def test_invalid_name(self):
        customer = Customer(
            name="Test2",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertNotEqual(error, None)
        self.assertNotIn(customer, db.session)

    def test_invalid_email(self):
        customer = Customer(
            name="Test two",
            email="testemail.com",
            phone="222 456 7890",
            address="Test2 address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertNotEqual(error, None)
        self.assertNotIn(customer, db.session)

    def test_invalid_phone(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222A 456 7890",
            address="Test2 address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertNotEqual(error, None)
        self.assertNotIn(customer, db.session)

    def test_address(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 456 7890",
            address="29 #34 at apt.2 LINE ONE house 65B"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.add()

        self.assertEqual(error, None)
        self.assertIn(customer, db.session)


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
