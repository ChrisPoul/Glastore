from .setup import MyTest
from Glastore.models import Window, db, repeated_value_msg


def make_test_window(name="Test"):
    window = Window(
        name=f"{name}",
        modelo="Test modelo"
    )
    error = window.add()
    if error:
        return window, error

    return window


class WindowsView(MyTest):

    def test_view(self):
        response = self.client.get(
            '/window/windows'
        )
        self.assertEqual(response.status_code, 200)

    def test_windows(self):
        make_test_window()
        make_test_window("Test 2")
        response = self.client.get(
            '/window/windows'
        )
        self.assertIn(b'Test', response.data)
        self.assertIn(b'Test 2', response.data)


class AddWindow(MyTest):

    def test_add(self):
        window = Window(
            name="Test"
        )
        error = window.add()
        assert window in db.session
        assert error is None

    def test_repeated_name(self):
        make_test_window("Test")
        window2, error = make_test_window("Test")
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
        window = make_test_window()
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
        window = make_test_window()
        window.name = "New Test"
        window.update()
        assert Window.get(1).name == "New Test"

    def test_repeated_name(self):
        window = make_test_window()
        make_test_window("Test2")
        window.name = "Test2"
        error = window.update()
        assert error == repeated_value_msg
        assert window.name == "Test"

    def test_modelo(self):
        window = make_test_window()
        window.modelo = "Modelo"
        error = window.update()
        assert window.modelo == "Modelo"
        assert error is None

    def test_pickletype(self):
        window = make_test_window()
        window.herrajes = ["Herraje"]
        window.update()
        assert window.herrajes == ["Herraje"]


class UpdateWindowView(MyTest):

    def test_view(self):
        make_test_window()
        response = self.client.get(
            '/window/update/1'
        )
        self.assertIn(b'Test', response.data)

    def test_update(self):
        window = make_test_window()
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
        window = make_test_window()
        window.delete()
        assert window not in db.session


class DeleteWindowView(MyTest):

    def test_delete(self):
        window = make_test_window()
        response = self.client.post(
            '/window/delete/1'
        )
        self.assertRedirects(response, '/window/windows')
        assert window not in db.session


class GetWindow(MyTest):

    def test_get(self):
        window = make_test_window()
        assert Window.get(1) == window

    def test_with_name(self):
        window = make_test_window()
        assert Window.get("Test") == window


class GetWindows(MyTest):

    def test_get_all(self):
        window = make_test_window()
        window2 = make_test_window("Test2")
        assert Window.get_all() == [window, window2]

    def test_with_modelo(self):
        window = make_test_window()
        window2 = make_test_window("Test2")
        assert Window.get_all("Test modelo") == [window, window2]

    def test_with_color(self):
        make_test_window()
        window = make_test_window("Test2")
        window.color = "Test color"
        assert Window.get_all("Test color") == [window]

    def test_with_cristal(self):
        window = make_test_window()
        window.cristal = "Test cristal"
        window2 = make_test_window("Test2")
        window2.cristal = "Test cristal"
        assert Window.get_all("Test cristal") == [window, window2]

    def test_with_acabado(self):
        window = make_test_window()
        window.acabado = "Test acabado"
        make_test_window("Test2")
        assert Window.get_all("Test acabado") == [window]

    def test_with_sellado(self):
        window = make_test_window()
        window.sellado = "Test sellado"
        make_test_window("Test2")
        assert Window.get_all("Test sellado") == [window]

    def test_with_material(self):
        window = make_test_window()
        window.material = "Test material"
        make_test_window("Test2")
        assert Window.get_all("Test material") == [window]
