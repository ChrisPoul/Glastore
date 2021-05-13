from .setup import MyTest
from flask import url_for
from Glastore.models.quote import Quote
from Glastore.models.customer import Customer
from Glastore.models.product import Product
from Glastore.models.quote.validation import QuoteValidation


class QuoteValidationTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.quote = Quote.new(1)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()
        self.product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        self.product.add()


class TestValidate(QuoteValidationTest):

    def test_should_not_return_error_given_valid_quote_quote(self):
        quote_validation = QuoteValidation(self.quote)
        self.quote.address = "Valid address"
        self.customer.name = "Valid customer"
        self.product.name = "Valid product"
        error = quote_validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_quote_data(self):
        quote_validation = QuoteValidation(self.quote)
        self.quote.address = ""
        self.customer.name = "1invalid name"
        self.product.name = ""
        error = quote_validation.validate()

        self.assertNotEqual(error, None)


class TestValidateAddress(QuoteValidationTest):

    def test_should_not_return_error_given_valid_address(self):
        quote_validation = QuoteValidation(self.quote)
        self.quote.address = "An address"
        error = quote_validation.validate_address()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_address(self):
        quote_validation = QuoteValidation(self.quote)
        self.quote.address = ""
        error = quote_validation.validate_address()

        self.assertNotEqual(error, None)


class TestValidateCustomer(QuoteValidationTest):

    def test_should_not_return_error_given_valid_customer(self):
        quote_validation = QuoteValidation(self.quote)
        self.customer.name = "Valid name"
        self.customer.email = "valid_email@email.com"
        error = quote_validation.validate_customer()

        self.assertEqual(error, None)


    def test_should_return_error_given_invalid_customer(self):
        quote_validation = QuoteValidation(self.quote)
        self.customer.name = ""
        self.customer.email = "test.email.com"
        error = quote_validation.validate_customer()

        self.assertNotEqual(error, None)


class TestValidateProducts(QuoteValidationTest):

    def test_should_not_return_error_given_valid_products(self):
        quote_validation = QuoteValidation(self.quote)
        product = Product(
            quote_id=1,
            name="Valid name",
            material="Valid Material",
            acabado="Valid Acabado",
            cristal="Valid Cristal"
        )
        product.add()
        error = quote_validation.validate_products()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_products(self):
        quote_validation = QuoteValidation(self.quote)
        product = Product(
            quote_id=1,
            name="",
            material="",
            acabado="",
            cristal=""
        )
        product.add()
        error = quote_validation.validate_products()
