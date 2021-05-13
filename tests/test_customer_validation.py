from .setup import MyTest
from Glastore.models.customer import Customer
from Glastore.models.customer.validation import CustomerValidation


class CustomerValidationTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()


class TestValidate(CustomerValidationTest):

    def test_should_not_return_error_given_valid_customer(self):
        customer_validation = CustomerValidation(self.customer)
        error = customer_validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_customer(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.name = ""
        error = customer_validation.validate()

        self.assertNotEqual(error, None)


class TestCheckForEmptyValues(CustomerValidationTest):

    def test_should_return_error_given_empty_name(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.name = ""
        error = customer_validation.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_email(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.email = ""
        error = customer_validation.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_phone(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.phone = ""
        error = customer_validation.check_for_emtpy_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_address(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.address = ""
        error = customer_validation.check_for_emtpy_values()

        self.assertNotEqual(error, None)


class TestCheckForRepeatedValues(CustomerValidationTest):

    def test_should_not_return_error_given_new_values(self):
        customer = Customer(
            name="Test two",
            email="test2@email.com",
            phone="222 4444 7777",
            address="Test address two"
        )
        customer_validation = CustomerValidation(customer)
        error = customer_validation.check_for_repeated_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_values(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7891",
            address="Test address"
        )
        customer_validation = CustomerValidation(customer)
        error = customer_validation.check_for_repeated_values()

        self.assertNotEqual(error, None)


class TestCheckForRepeatedValue(CustomerValidationTest):

    def setUp(self):
        CustomerValidationTest.setUp(self)
        self.customer2 = Customer(
            name="Test two",
            email="test2@email.com",
            phone="321 654 0987",
            address="Test address two"
        )
        self.customer2.add()

    def test_should_not_return_error_given_not_repeated_value(self):
        customer_validation = CustomerValidation(self.customer2)
        error = customer_validation.check_for_repeated_value("Test two")

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        customer_validation = CustomerValidation(self.customer2)
        error = customer_validation.check_for_repeated_value("Test")

        self.assertNotEqual(error, None)


class TestValidateName(CustomerValidationTest):

    def test_validate_name(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.name = "New Name"
        error = customer_validation.validate_name()

        self.assertEqual(error, None)

    def test_invalid_name(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.name = "Test2"
        error = customer_validation.validate_name()

        self.assertNotEqual(error, None)


class TestValidateEmail(CustomerValidationTest):

    def test_validate_email(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.email = "new@email.com"
        error = customer_validation.validate_email()

        self.assertEqual(error, None)

    def test_invalid_email(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.email = "test.email.com"
        error = customer_validation.validate_email()

        self.assertNotEqual(error, None)


class TestValidatePhone(CustomerValidationTest):

    def test_validate_phone(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.phone = "442 300 1411"
        error = customer_validation.validate_phone()

        self.assertEqual(error, None)

    def test_with_plus_sign(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.phone = "+442 300 1411"
        error = customer_validation.validate_phone()

        self.assertEqual(error, None)

    def test_invalid_phone(self):
        customer_validation = CustomerValidation(self.customer)
        self.customer.phone = "string"
        error = customer_validation.validate_phone()

        self.assertNotEqual(error, None)
