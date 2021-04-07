from .setup import MyTest
from Glastore.models import db
from Glastore.models.product import Product


class ProductTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.product = Product(
            name="Test Product",
            material="Test Material",
            acabado="Test Acabado",
            cristal="Test Cristal",
            unit_price=10
        )
        self.product.add()


class ProductsView(ProductTest):

    def test_view(self):
        response = self.client.get(
            '/product/products'
        )
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        Product.new("Test 2")
        response = self.client.get(
            '/product/products'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Test 2', response.data)


class AddProduct(ProductTest):

    def test_add(self):
        product = Product(
            name="Test 2"
        )
        error = product.add()
        assert product in db.session
        assert error is None

    def test_repeated_name(self):
        product = Product(
            name="Test2"
        )
        product.add()
        product2 = Product(
            name="Test2"
        )
        error = product2.add()
        assert product2 in db.session
        self.assertEqual(error, None)

    def test_price(self):
        product = Product(
            name="Test 2",
            unit_price=10
        )
        error = product.add()
        self.assertEqual(error, None)
        self.assertEqual(product.unit_price, 10.0)


class AddProductView(ProductTest):

    def test_view(self):
        response = self.client.get(
            '/product/add'
        )
        self.assertIn(b'Agregar Producto', response.data)

    def test_add(self):
        data = dict(
            name="Test2",
            material="test material",
            acabado="test acabado",
            cristal="test cristal"
        )
        response = self.client.post(
            '/product/add',
            data=data
        )
        self.assertRedirects(response, '/product/products')


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


class UpdateProductView(ProductTest):

    def test_view(self):
        response = self.client.get(
            '/product/update/1'
        )
        self.assertIn(b'Test', response.data)

    def test_update(self):
        data = dict(
            name="Changed Name",
            material="test material",
            acabado="un acabado",
            cristal="test cristal"
        )
        response = self.client.post(
            '/product/update/1',
            data=data
        )
        self.assertRedirects(response, '/product/products')
        assert self.product.name == "Changed Name"


class DeleteProduct(ProductTest):

    def test_delete(self):
        self.product.delete()
        assert self.product not in db.session

    def test_view(self):
        response = self.client.post(
            '/product/delete/1'
        )
        self.assertRedirects(response, '/product/products')
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
