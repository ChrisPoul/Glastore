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

    def test_should_add_product_given_valid_product(self):
        product = Product(
            quote_id=1,
            name="Test two",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(product)
        product_request.add()

        self.assertIn(product, self.db.session)

    def test_should_not_add_product_given_invalid_product(self):
        product = Product(
            quote_id=1,
            name="",
            material="",
            acabado="",
            cristal=""
        )
        product_request = ProductRequest(product)
        product_request.add()

        self.assertNotIn(product, self.db.session)


class TestUpdate(ProductRequestTest):

    def setUp(self):
        ProductRequestTest.setUp(self)
        self.product2 = Product(
            quote_id=1,
            name="Test2",
            material="Material2",
            acabado="Acabado2",
            cristal="Cristal2"
        )
        self.product2.add()

    def test_should_update_product_given_valid_data(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="New Name",
            material1="Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, product_data):
            product_request.update()
        self.db.session.rollback()

        self.assertEqual(self.product.name, "New Name")

    def test_should_not_update_product_given_invalid_data(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="",
            material1="",
            acabado1="",
            cristal1=""
        )
        with self.request_context(url, product_data):
            product_request.update()
        self.db.session.rollback()

        self.assertEqual(self.product.name, "Test")


class TestUpdateAttributes(ProductRequestTest):

    def test_should_update_attributes_given_valid_data(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="New Name",
            material1="New Material",
            acabado1="New Acabado",
            cristal1="New Cristal"
        )
        with self.request_context(url, product_data):
            product_request.update_attributes()

        self.assertEqual(self.product.name, "New Name")
        self.assertEqual(self.product.material, "New Material")
        self.assertEqual(self.product.acabado, "New Acabado")
        self.assertEqual(self.product.cristal, "New Cristal")

    def test_should_update_attributes_given_invalid_data(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="",
            material1="",
            acabado1="",
            cristal1=""
        )
        with self.request_context(url, product_data):
            product_request.update_attributes()

        self.assertEqual(self.product.name, "")
        self.assertEqual(self.product.material, "")
        self.assertEqual(self.product.acabado, "")
        self.assertEqual(self.product.cristal, "")

    def test_should_not_save_changes(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="New Name"
        )
        with self.request_context(url, product_data):
            product_request.update_attributes()
        self.db.session.rollback()

        self.assertEqual(self.product.name, "Test")


class TestUpdateAttribute(ProductRequestTest):

    def test_should_update_name_given_name_as_argument(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="New Name",
            material1="New Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, product_data):
            product_request.update_attribute("name")

        self.assertEqual(self.product.name, "New Name")
        self.assertEqual(self.product.material, "Material")

    def test_should_update_name_given_material_as_argument(self):
        product_request = ProductRequest(self.product)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name1="New Name",
            material1="New Material",
            acabado1="Acabado",
            cristal1="Cristal"
        )
        with self.request_context(url, product_data):
            product_request.update_attribute("material")

        self.assertEqual(self.product.name, "Test")
        self.assertEqual(self.product.material, "New Material")


class TestUpdateTotal(ProductRequestTest):

    def test_should_update_total_given_valid_numbers(self):
        self.product.unit_price = 10
        product_request = ProductRequest(self.product)
        self.product.cantidad = 5
        product_request.update_total()

        self.assertEqual(self.product.total, 50)
