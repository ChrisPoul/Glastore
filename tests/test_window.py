from .setup_tests import MyTest
from Glastore.models import Window, db, repeated_value_msg


class AddWindow(MyTest):

    def test_add(self):
        window = Window(
            name="Test"
        )
        error = window.add()
        assert window in db.session
        assert error is None

    def test_repeated_name(self):
        window = Window(
            name="Test"
        )
        window.add()
        window2 = Window(
            name="Test"
        )
        error = window2.add()
        assert window2 not in db.session
        assert error == repeated_value_msg

    def test_empty_values(self):
        window = Window(
            name="Test"
        )
        window.add()
        window2 = Window(
            name="Test2"
        )
        window2.add()
        assert window in db.session
        assert window2 in db.session

    def test_big_description(self):
        long_text = "some text"
        for _ in range(8):
            long_text += long_text
        window = Window(
            name="Test",
            description=long_text
        )
        error = window.add()
        assert window in db.session
        assert error is None

    def test_pickletype(self):
        window = Window(
            name="Test"
        )
        window.add()
        assert window.herrajes == []


class AddWindowView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/window/add'
        )
        self.assertIn(b'Agregar Ventana', response.data)

    def test_add(self):
        data = dict(
            name="Test"
        )
        response = self.client.post(
            '/window/add',
            data=data
        )
        self.assertRedirects(response, '/window/windows')


class UpdateWindow(MyTest):

    def test_update(self):
        window = Window(
            name="Test"
        )
        window.add()
        window.name = "New Test"
        window.update()
        assert Window.get(1).name == "New Test"

    def test_repeated_name(self):
        window = Window(
            name="Test"
        )
        window.add()
        window2 = Window(
            name="Test2"
        )
        window2.add()
        window.name = "Test2"
        error = window.update()
        assert error == repeated_value_msg
        assert window.name == "Test"

    def test_modelo(self):
        window = Window(
            name="Test"
        )
        window.add()
        window.modelo = "Modelo"
        error = window.update()
        assert error is None
        assert window.modelo == "Modelo"

    def test_pickletype(self):
        window = Window(
            name="Test"
        )
        window.add()
        window.herrajes = ["Herraje"]
        window.update()
        assert window.herrajes == ["Herraje"]


class UpdateWindowView(MyTest):

    def test_view(self):
        window = Window(
            name="Test",
            material="Un material"
        )
        window.add()
        response = self.client.get(
            '/window/update/1'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Un material', response.data)

    def test_update(self):
        window = Window(
            name="Test"
        )
        window.add()
        data = dict(
            name="Changed Name"
        )
        response = self.client.post(
            '/window/update/1',
            data=data
        )
        self.assertRedirects(response, '/window/windows')
        assert window.name == "Changed Name"


class DeleteWindow(MyTest):

    def test_delete(self):
        window = Window(
            name="Test"
        )
        window.add()
        window.delete()
        assert window not in db.session


class DeleteWindowView(MyTest):

    def test_delete(self):
        window = Window(
            name="Test"
        )
        window.add()
        response = self.client.post(
            '/window/delete/1'
        )
        self.assertRedirects(response, '/window/windows')
        assert window not in db.session


class GetWindow(MyTest):

    def test_get(self):
        window = Window(
            name="Test"
        )
        window.add()
        assert Window.get(1) == window

    def test_with_name(self):
        window = Window(
            name="Test"
        )
        window.add()
        assert Window.get("Test") == window


class GetWindows(MyTest):

    def test_get_all(self):
        window = Window(
            name="Test"
        )
        window.add()
        window2 = Window(
            name="Test2"
        )
        window2.add()
        assert Window.get_all() == [window, window2]

    def test_with_modelo(self):
        window = Window(
            name="Test",
            modelo="Modelo"
        )
        window.add()
        window2 = Window(
            name="Test2",
            modelo="Modelo"
        )
        window2.add()
        assert Window.get_all("Modelo") == [window, window2]

    def test_with_color(self):
        window = Window(
            name="Test",
            color="Color"
        )
        window.add()
        window2 = Window(
            name="Test2",
            color="Color"
        )
        window2.add()
        assert Window.get_all() == [window, window2]

    def test_with_cristal(self):
        window = Window(
            name="Test",
            cristal="Cristal"
        )
        window.add()
        window2 = Window(
            name="Test2",
            cristal="Cristal"
        )
        window2.add()
        assert Window.get_all("Cristal") == [window, window2]

    def test_with_acabado(self):
        window = Window(
            name="Test",
            acabado="acabado"
        )
        window.add()
        window2 = Window(
            name="Test2",
            acabado="acabado"
        )
        window2.add()
        assert Window.get_all("acabado") == [window, window2]

    def test_with_sellado(self):
        window = Window(
            name="Test",
            sellado="sellado"
        )
        window.add()
        window2 = Window(
            name="Test2",
            sellado="sellado"
        )
        window2.add()
        assert Window.get_all("sellado") == [window, window2]

    def test_with_material(self):
        window = Window(
            name="Test",
            material="material"
        )
        window.add()
        window2 = Window(
            name="Test2",
            material="material"
        )
        window2.add()
        assert Window.get_all("material") == [window, window2]
