from flask import url_for
from .setup import MyTest
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

    def test_should_add_customer_given_valid_customer(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer_request = CustomerRequest(customer)
        customer_request.add()
        self.db.session.rollback()

        self.assertIn(customer, self.db.session)

    def test_should_not_add_customer_given_invalid_customer(self):
        customer = Customer(
            name="",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer_request = CustomerRequest(customer)
        customer_request.add()
        self.db.session.rollback()

        self.assertNotIn(customer, self.db.session)


class TestUpdate(CustomerRequestTest):

    def test_should_update_given_valid_data(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', id=self.customer.id)
        customer_data = dict(
            name="New Name",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, customer_data):
            customer_request.update()
        self.db.session.rollback()

        self.assertEqual(self.customer.name, "New Name")

    def test_should_not_update_given_invalid_data(self):
        customer_request = CustomerRequest(self.customer)
        url = url_for('customer.update', id=self.customer.id)
        customer_data = dict(
            name="",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        with self.request_context(url, customer_data):
            customer_request.update()
        self.db.session.rollback()

        self.assertEqual(self.customer.name, "Test")


class TestUpdateAttributes(CustomerRequestTest):

    def setUp(self):
        CustomerRequestTest.setUp(self)
        self.customer2 = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test address 2"
        )
        self.customer2.add()

    def test_should_update_attributes_given_valid_data(self):
        customer_request = CustomerRequest(self.customer2)
        url = url_for('customer.update', id=self.customer2.id)
        customer_data = dict(
            name="New Name",
            email="test2@email.com",
            phone="222 456 7890",
            address="Test address 2"
        )
        with self.request_context(url, customer_data):
            customer_request.update_attributes()

        self.assertEqual(self.customer2.name, "New Name")

    def test_should_update_attributes_given_invalid_data(self):
        customer_request = CustomerRequest(self.customer2)
        url = url_for('customer.update', id=self.customer2.id)
        customer_data = dict(
            name="Test",
            email="test.email.com",
            phone="invalid phone",
            address=""
        )
        with self.request_context(url, customer_data):
            customer_request.update_attributes()

        self.assertEqual(self.customer.name, "Test")
        self.assertEqual(self.customer2.email, "test.email.com")
        self.assertEqual(self.customer2.phone, "invalid phone")
        self.assertEqual(self.customer2.address, "")

    def test_should_not_save_changes_given_any_data(self):
        customer_request = CustomerRequest(self.customer2)
        url = url_for('customer.update', id=self.customer2.id)
        customer_data = dict(
            name="New Name"
        )
        with self.request_context(url, customer_data):
            customer_request.update_attributes()
        self.db.session.rollback()

        self.assertEqual(self.customer2.name, "Test two")


class TestValidate(CustomerRequestTest):

    def test_should_not_return_error_given_valid_customer(self):
        customer_request = CustomerRequest(self.customer)
        error = customer_request.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_customer(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = ""
        error = customer_request.validate()

        self.assertNotEqual(error, None)


class TestCheckForEmptyValues(CustomerRequestTest):

    def test_should_return_error_given_empty_name(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.name = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_email(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.email = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_phone(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.phone = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_address(self):
        customer_request = CustomerRequest(self.customer)
        self.customer.address = ""
        error = customer_request.check_for_emtpy_values()

        self.assertNotEqual(error, None)


class TestCheckForRepeatedValues(CustomerRequestTest):

    def test_should_not_return_error_given_new_values(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 4444 7777",
            address="Test address two"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.check_for_repeated_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_values(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7891",
            address="Test address"
        )
        customer_request = CustomerRequest(customer)
        error = customer_request.check_for_repeated_values()

        self.assertNotEqual(error, None)


class TestCheckForRepeatedValue(CustomerRequestTest):

    def setUp(self):
        CustomerRequestTest.setUp(self)
        self.customer2 = Customer(
            name="Test two",
            email="test2@email.com",
            phone="321 654 0987",
            address="Test address two"
        )
        self.customer2.add()

    def test_should_not_return_error_given_not_repeated_value(self):
        customer_request = CustomerRequest(self.customer2)
        error = customer_request.check_for_repeated_value("Test two")

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        customer_request = CustomerRequest(self.customer2)
        error = customer_request.check_for_repeated_value("Test")

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
