from .setup import MyTest
from Glastore.models import db
from Glastore.models.product import Product


class ProductTest(MyTest):

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


class TestAdd(ProductTest):

    def test_add(self):
        product = Product(
            quote_id=1,
            name="Test2",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()

        self.assertIn(product, db.session)

    def test_repeated_name(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()

        self.assertIn(product, db.session)


class TestUpdate(ProductTest):

    def test_update(self):
        self.product.name = "New Name"
        self.product.update()

        self.assertEqual(self.product.name, "New Name")

    def test_repeated_name(self):
        product = Product(
            quote_id=1,
            name="Test2",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()
        product.name = "Test"
        product.update()

        self.assertEqual(product.name, "Test")


class TestDelete(ProductTest):

    def test_delete(self):
        self.product.delete()

        self.assertNotIn(self.product, db.session)

