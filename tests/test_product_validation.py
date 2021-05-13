from .setup import MyTest
from flask import url_for
from Glastore.models.product import Product
from Glastore.models.product.validation import ProductValidation
from Glastore.models.quote import Quote


class ProductRequestTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        self.product.add()
        self.quote = Quote.new(1)


class TestValidate(ProductRequestTest):

    def test_should_not_return_error_given_valid_product(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price=10,
            cantidad=1
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_product(self):
        product = Product(
            quote_id=1,
            name="",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price="invalid price",
            cantidad="invalid cantidad"
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_given_repeated_values(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()
        product_validation = ProductValidation(product)
        error = product_validation.validate()

        self.assertEqual(error, None)


class TestCheckForEmptyValues(ProductRequestTest):

    def test_should_not_return_error_given_non_empty_values(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_validation = ProductValidation(product)
        error = product_validation.check_for_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_values(self):
        product = Product(
            quote_id=1,
            name="",
            material="",
            acabado="",
            cristal=""
        )
        product_validation = ProductValidation(product)
        error = product_validation.check_for_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUnitPrice(ProductRequestTest):

    def test_should_not_return_error_given_valid_unit_price(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price=10.0
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate_unit_price()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_unit_price(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price="invalid unit_price"
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate_unit_price()

        self.assertNotEqual(error, None)


class TestValidateCantidad(ProductRequestTest):

    def test_should_not_return_error_given_valid_cantidad(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            cantidad=1
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate_cantidad()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_cantidad(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            cantidad="invalid cantidad"
        )
        product_validation = ProductValidation(product)
        error = product_validation.validate_cantidad()

        self.assertNotEqual(error, None)
