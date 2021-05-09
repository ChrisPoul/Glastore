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
        self.customer.name = ""
        error = customer_request.validate()

        self.assertNotEqual(error, None)

    def test_invalid_value(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = "Test2"
        error = customer_request.validate()

        self.assertNotEqual(error, None)


class TestCheckForEmptyValues(CustomerRequestTest):

    def test_empty_name(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_empty_email(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.email = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_emtpy_phone(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.phone = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)


class TestValidateName(CustomerRequestTest):

    def test_validate_name(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = "New Name"
        error = customer_request.validate_name()

        self.assertEqual(error, None)

    def test_invalid_name(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = "Test2"
        error = customer_request.validate_name()

        self.assertNotEqual(error, None)


class TestValidateEmail(CustomerRequestTest):

    def test_validate_email(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.email = "new@email.com"
        error = customer_request.validate_email()

        self.assertEqual(error, None)

    def test_invalid_email(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.email = "test.email.com"
        error = customer_request.validate_email()

        self.assertNotEqual(error, None)


class TestValidatePhone(CustomerRequestTest):

    def test_validate_phone(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.phone = "442 300 1411"
        error = customer_request.validate_phone()

        self.assertEqual(error, None)

    def test_with_plus_sign(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.phone = "+442 300 1411"
        error = customer_request.validate_phone()

        self.assertEqual(error, None)

    def test_invalid_phone(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.phone = "string"
        error = customer_request.validate_phone()

        self.assertNotEqual(error, None)
