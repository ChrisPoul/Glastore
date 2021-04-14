from .setup import MyTest
from Glastore.models import db
from Glastore.models.window import Window


class WindowTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.window = Window(
            product_id=1,
            description="a meaningless description"
        )
        self.window.add()


class TestBasicWindowMethods(MyTest):

    def test_add(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        self.assertIn(window, db.session)

    def test_update(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        window.description = "another description"
        window.update()
        self.assertEqual(window.description, "another description")

    def test_remove(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        window.delete()
        self.assertNotIn(window, db.session)

    def test_get(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        self.assertEqual(Window.get(1), window)
        self.assertEqual(Window.get(2), None)

    
class TestWindowProperies(WindowTest):

    def test_name_with_no_dimensions(self):
        self.window.description = "una ventana random"
        self.assertEqual(self.window.name, "una ventana random")

    def test_name_with_dimensions(self):
        self.window.description = "una ventana random 10x10"
        self.assertEqual(self.window.name, "una ventana random ")

    def test_dimensions(self):
        self.window.description = "una ventana random 10x10"
        self.assertEqual(self.window.dimensions, (10, 10))


class TestWindowMethods(WindowTest):

    def test_update_description(self):
        self.window.update_description("nueva descripcion")
        self.assertEqual(self.window.description, "nueva descripcion")

    def test_extract_dimensions_string(self):
        self.window.description = "una ventana random de 10 x 10"
        self.assertEqual(self.window.extract_dimensions_string(), "10 x 10")

    def test_get_width_and_height(self):
        dimensions = self.window.get_width_and_height("10x10")
        self.assertEqual(dimensions, (10, 10))

    def test_get_width(self):
        dimensions = "15x20"
        separator = "x"
        width = self.window.get_width(dimensions, separator)
        self.assertEqual(width, 15)

    def test_get_height(self):
        dimensions = "15x20"
        separator = "x"
        width = self.window.get_height(dimensions, separator)
        self.assertEqual(width, 20)

    def test_has_dimensions_false(self):
        self.window.description = "ventana sin medidas"
        self.assertEqual(self.window.has_dimensions(), False)

    def test_has_dimensions_true(self):
        self.window.description = "ventana con medidas 72x68"
        self.assertEqual(self.window.has_dimensions(), True)
