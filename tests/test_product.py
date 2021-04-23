from .setup import MyTest, make_test_customer
from Glastore.models import db
from Glastore.models.product import Product
from Glastore.models.quote import Quote


class ProductTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = make_test_customer()
        self.product = Product(
            quote_id=1,
            name="Test Product",
            material="Test Material",
            acabado="Test Acabado",
            cristal="Test Cristal",
            unit_price=10
        )
        self.product.add()
        self.quote = Quote.new(self.customer.id)


class AddProduct(ProductTest):

    def test_add(self):
        product = Product(
            quote_id=1,
            name="Test 2"
        )
        error = product.add()
        self.assertEqual(error, None)
        assert product in db.session

    def test_repeated_name(self):
        product = Product(
            quote_id=1,
            name="Test2"
        )
        product.add()
        product2 = Product(
            quote_id=1,
            name="Test2"
        )
        error = product2.add()
        self.assertEqual(error, None)
        assert product2 in db.session

    def test_price(self):
        product = Product(
            quote_id=1,
            name="Test 2",
            unit_price=10
        )
        error = product.add()
        self.assertEqual(error, None)
        self.assertEqual(product.unit_price, 10.0)


class UpdateProduct(ProductTest):

    def test_update(self):
        self.product.name = "New Test"
        self.product.update()
        assert self.product.name == "New Test"

    def test_repeated_name(self):
        product = Product.new("Test2")
        product.name = "Test Product"
        error = product.update()
        self.assertEqual(error, None)
        assert product.name == "Test Product"


class DeleteProduct(ProductTest):

    def test_delete(self):
        self.product.delete()
        assert self.product not in db.session


class GetProduct(ProductTest):

    def test_get(self):
        assert Product.get(1) == self.product

    def test_with_name(self):
        assert Product.get("Test Product") == self.product


class GetProducts(ProductTest):

    def test_get_all(self):
        product2 = Product.new("Test2")
        assert Product.get_all() == [self.product, product2]

    def test_with_cristal(self):
        self.product.cristal = "Test cristal"
        product2 = Product.new("Test2")
        product2.cristal = "Test cristal"
        assert Product.get_all("Test cristal") == [self.product, product2]

    def test_with_material(self):
        self.product.material = "Test material"
        Product.new("Test2")
        assert Product.get_all("Test material") == [self.product]


class UpdateOnSumbit(ProductTest):

    def test_update_product_on_submit(self):
        self.quote.add_product(self.product)
        data = dict(
            material1="New Material"
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            self.product.request.update()
        self.assertEqual(self.product.material, "New Material")

    def test_update_attributes_on_submit(self):
        self.quote.add_product(self.product)
        data = dict(
            cantidad1=1
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            self.product.request.update_attributes()
        self.assertEqual(self.product.cantidad, str(1))

    def test_update_total(self):
        self.product.cantidad = 1
        self.product.update_total()
        self.assertEqual(self.product.total, 10)
