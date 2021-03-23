from .setup import MyTest
from Glastore.models import Product, db, repeated_value_msg


class ProductsView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/product/products'
        )
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        Product.new("Test")
        Product.new("Test 2")
        response = self.client.get(
            '/product/products'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Test 2', response.data)


class AddProduct(MyTest):

    def test_add(self):
        product = Product(
            name="Test"
        )
        error = product.add()
        assert product in db.session
        assert error is None

    def test_repeated_name(self):
        Product.new("Test")
        product2, error = Product.new("Test")
        assert product2 not in db.session
        assert error == repeated_value_msg

    def test_empty_values(self):
        product = Product(
            name="Test"
        )
        product.add()
        product2 = Product(
            name="Test2"
        )
        product2.add()
        assert product in db.session
        assert product2 in db.session


class AddProductView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/product/add'
        )
        self.assertIn(b'Agregar Producto', response.data)

    def test_add(self):
        data = dict(
            name="Test"
        )
        response = self.client.post(
            '/product/add',
            data=data
        )
        self.assertRedirects(response, '/product/products')


class UpdateProduct(MyTest):

    def test_update(self):
        product = Product.new("Test")
        product.name = "New Test"
        product.update()
        assert Product.get(1).name == "New Test"

    def test_repeated_name(self):
        product = Product.new("Test")
        Product.new("Test2")
        product.name = "Test2"
        error = product.update()
        assert error == repeated_value_msg
        assert product.name == "Test"


class UpdateProductView(MyTest):

    def test_view(self):
        Product.new("Test")
        response = self.client.get(
            '/product/update/1'
        )
        self.assertIn(b'Test', response.data)

    def test_update(self):
        product = Product.new("Test")
        data = dict(
            name="Changed Name"
        )
        response = self.client.post(
            '/product/update/1',
            data=data
        )
        self.assertRedirects(response, '/product/products')
        assert product.name == "Changed Name"


class DeleteProduct(MyTest):

    def test_delete(self):
        product = Product.new("Test")
        product.delete()
        assert product not in db.session


class DeleteProductView(MyTest):

    def test_delete(self):
        product = Product.new("Test")
        response = self.client.post(
            '/product/delete/1'
        )
        self.assertRedirects(response, '/product/products')
        assert product not in db.session


class GetProduct(MyTest):

    def test_get(self):
        product = Product.new("Test")
        assert Product.get(1) == product

    def test_with_name(self):
        product = Product.new("Test")
        assert Product.get("Test") == product


class GetProducts(MyTest):

    def test_get_all(self):
        product = Product.new("Test")
        product2 = Product.new("Test2")
        assert Product.get_all() == [product, product2]

    def test_with_cristal(self):
        product = Product.new("Test")
        product.cristal = "Test cristal"
        product2 = Product.new("Test2")
        product2.cristal = "Test cristal"
        assert Product.get_all("Test cristal") == [product, product2]

    def test_with_material(self):
        product = Product.new("Test")
        product.material = "Test material"
        Product.new("Test2")
        assert Product.get_all("Test material") == [product]
