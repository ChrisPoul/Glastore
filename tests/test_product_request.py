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
        url = url_for('quote.edit', quote_id=self.quote.id)
        data = dict(
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product_request = ProductRequest(self.product)
        with self.request_context(url, data):
            error = product_request.add()

        self.assertEqual(error, None)
