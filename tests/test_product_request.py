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


class TestUpdate(ProductRequestTest):

    def test_update(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name1="New Name",
            material1="Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, data):
            error = product_request.update()

        self.assertEqual(error, None)
        self.assertEqual(self.product.name, "New Name")

    def test_update_attributes(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name1="New Name",
            material1="New Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, data):
            product_request.update_attributes()

        self.assertEqual(self.product.name, "New Name")
        self.assertEqual(self.product.material, "New Material")

    def test_update_attribute(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name1="New Name",
            material1="New Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, data):
            product_request.update_attribute("name")

        self.assertEqual(self.product.name, "New Name")
        self.assertEqual(self.product.material, "Material")

    def update_total(self):
        product_request = ProductRequest(self.product)
        self.product.cantidad = "2"
        self.product.unit_price = 10
        product_request.update_total()

        self.assertEqual(self.product.total, 20)


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

    def test_empty_value(self):
        product_request = ProductRequest(self.product)
        self.product.name = ""
        error = product_request.validate()

        self.assertNotEqual(error, None)

    def test_repeated_values(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()
        product_request = ProductRequest(product)
        error = product_request.validate()

        self.assertEqual(error, None)


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
