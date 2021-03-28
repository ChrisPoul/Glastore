from .setup import MyTest
from Glastore.models import db
from Glastore.models.quote import SoldProduct


class TestSoldProduct(MyTest):

    def test_add(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        error = sold_product.add()
        self.assertIn(sold_product, db.session)
        self.assertEqual(error, None)

    def test_update(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        sold_product.total = 1
        error = sold_product.update()
        self.assertEqual(error, None)
        self.assertEqual(sold_product.total, 1.0)

    def test_get(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        self.assertEqual(SoldProduct.get(1), sold_product)


class EditOnSumbit(MyTest):

    def test_edit_product_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            material1="New Material"
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_product_on_submit()
        self.assertEqual(self.product.material, "New Material")

    def test_edit_cantidad_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            cantidad1=1
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_cantidad_on_submit()
        self.assertEqual(sold_product.cantidad, str(1))

    def test_update_total(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        sold_product.cantidad = 1
        sold_product.update_total()
        self.assertEqual(sold_product.total, 10)

    def edit_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            material1="Nuevo Material",
            cantidad1=1
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_on_submit()
        self.assertEqual(self.product.material, "Nuevo Material")
        self.assertEqual(sold_product.cantidad, 1)
        self.assertEqual(sold_product.total, 10)
