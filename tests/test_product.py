from .setup import MyTest
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

    def test_should_add_product_given_new_values(self):
        product = Product(
            quote_id=1,
            name="Test2",
            material="Material2",
            acabado="Acabado2",
            cristal="Cristal2"
        )
        product.add()

        self.assertIn(product, self.db.session)

    def test_should_add_product_given_repeated_values(self):
        product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        product.add()

        self.assertIn(product, self.db.session)

    def test_should_add_product_given_empty_values(self):
        product = Product(
            quote_id=1,
            name="",
            material="",
            acabado="",
            cristal=""
        )
        product.add()

        self.assertIn(product, self.db.session)


class TestUpdate(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        self.product2 = Product(
            quote_id=1,
            name="Test2",
            material="Material2",
            acabado="Acabado2",
            cristal="Cristal2"
        )
        self.product2.add()

    def test_should_update_product_given_valid_name(self):
        self.product.name = "New Name"
        self.product.update()
        self.db.session.rollback()

        self.assertEqual(self.product.name, "New Name")

    def test_should_update_product_given_repeated_name(self):
        self.product2.name = "Test"
        self.product2.update()
        self.db.session.rollback()

        self.assertEqual(self.product2.name, "Test")


class TestDelete(ProductTest):

    def test_should_delete_product(self):
        self.product.delete()

        self.assertNotIn(self.product, self.db.session)


class TestGet(ProductTest):

    def test_should_return_product_given_valid_id(self):
        product = Product.get(1)
        
        self.assertEqual(product, self.product)

    def test_should_return_none_given_invalid_id(self):
        product = Product.get(2)

        self.assertEqual(product, None)


class TestGetAll(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        self.product2 = Product(
            quote_id=1,
            name="Test2",
            material="Material2",
            acabado="Acabado2",
            cristal="Cristal2"
        )
        self.product2.add()

    def test_should_return_all_products(self):
        products = Product.get_all()

        self.assertEqual(products, [self.product, self.product2])
