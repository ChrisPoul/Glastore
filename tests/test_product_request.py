from .setup import MyTest
from flask import url_for
from Glastore.models.product import Product
from Glastore.models.product.request import ProductRequest
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


class TestAdd(ProductRequestTest):

    def test_add(self):
        product = Product(
            quote_id=1,
            name="Test two",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(product)
        error = product_request.add()

        self.assertEqual(error, None)
        self.assertIn(product, self.db.session)

    def test_repeated_name(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(product)
        error = product_request.add()

        self.assertEqual(error, None)
        self.assertEqual(Product.get_all(), [self.product, product])


class TestUpdate(ProductRequestTest):

    def test_update(self):
        pass


class TestValidate(ProductRequestTest):

    def test_valid_product(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(product)
        error = product_request.validate()

        self.assertEqual(error, None)

    def test_invalid_product(self):
        product = Product(
            quote_id=1,
            name="",
            material="",
            acabado="",
            cristal="",
            unit_price="string"
        )
        product_request = ProductRequest(product)
        error = product_request.validate()


class TestValidateAttributes(ProductRequestTest):

    def test_empty_name(self):
        product = Product(
            quote_id=1,
            name="",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(product)
        error = product_request.validate_attributes()

        self.assertNotEqual(error, None)

    def test_emtpy_values(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="",
            acabado="",
            cristal=""
        )
        product_request = ProductRequest(product)
        error = product_request.validate_attributes()

        self.assertNotEqual(error, None)


class TestValidateUnitPrice(ProductRequestTest):

    def test_valid_unit_price(self):
        product = Product(
            quote_id=1,
            name="",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price=10.0
        )
        product_request = ProductRequest(product)
        error = product_request.validate_unit_price()

        self.assertEqual(error, None)

    def test_invalid_unit_price(self):
        product = Product(
            quote_id=1,
            name="",
            material="Material",
            acabado="Acabado",
            cristal="Cristal",
            unit_price="string"
        )
        product_request = ProductRequest(product)
        error = product_request.validate_unit_price()

        self.assertNotEqual(error, None)
