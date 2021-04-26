from .setup import MyTest
from Glastore.models.window import Window
from Glastore.models.product.final_window.position import WindowPositioner


def make_test_window(description):
    window = Window(
        product_id=1,
        description=description
    )
    window.add()

    return window


class TestGetWindowPositions(MyTest):

    def test_simple_window(self):
        window = make_test_window("ventana fija de 10,10")
        windows = [window]
        positioner = WindowPositioner(windows)
        window_positions = positioner.get_window_positions()
        self.assertEqual(window_positions, [(0, 0)])

    def test_simple_windows(self):
        window1 = make_test_window("ventana corrediza 10,10")
        window2 = make_test_window("fija con dimenciones 10x10 con texto extra")
        windows = [window1, window2]
        positioner = WindowPositioner(windows)
        window_positions = positioner.get_window_positions()
        self.assertEqual(window_positions[0], (0, 0))
        self.assertEqual(window_positions[1], (10, 0))

    def test_window_on_top(self):
        window1 = make_test_window("ventana corrediza 15,15")
        window2 = make_test_window("fijo superior con dimenciones 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], (0, 0))
        self.assertEqual(positions[1], (0, 15))

    def test_window_on_bottom(self):
        window1 = make_test_window("ventana corrediza 15,15")
        window2 = make_test_window("fijo inferior con dimenciones 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], (0, 0))
        self.assertEqual(positions[1], (0, -10))

    def test_window_twice(self):
        pass

    def test_dos_fijos_laterales(self):
        window = make_test_window("puerta abatible de 10x15 con")
        lateral1 = make_test_window("dos fijos laterales de 5x15")
        lateral2 = make_test_window("fijos laterales de 5x15")
        positioner = WindowPositioner([window, lateral1, lateral2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions, [(5, 0), (0, 0), (15, 0)])

    def test_window_with_antepecho(self):
        window1 = make_test_window("puerta abatible de 15x15")
        window2 = make_test_window("antepecho fijo de 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], (0, 0))
        self.assertEqual(positions[1], (0, 15))

    def test_dos_laterales(self):
        pass


class TestHandleLaterales(MyTest):

    def test_dos_fijos_laterales(self):
        window = make_test_window("puerta abatible de 10x15 con")
        laterales = make_test_window("dos fijos laterales de 5x15")
        positioner = WindowPositioner([window, laterales])
        self.assertEqual(positioner.xposition, 0)
        positioner.handle_laterales()
        self.assertEqual(positioner.xposition, 5)


class TestAddWindowPositions(MyTest):

    def test_simple_window(self):
        window = make_test_window("ventana fija de 10x15")
        positioner = WindowPositioner([window])
        positioner.window_positions = []
        positioner.handle_laterales()
        positioner.add_window_positions()
        self.assertEqual(
            positioner.window_positions,
            [(0, 0)]
        )

class TestDecideWindowPosition(MyTest):

    def test_superior(self):
        window = make_test_window("puerta abatible de 10x15 con")
        superior = make_test_window("fijo superior de 5x15")
        positioner = WindowPositioner([window, superior])
        positioner.decide_window_position(superior)
        self.assertEqual(positioner.xposition, 0)
        self.assertEqual(positioner.yposition, 15)


