from .setup import MyTest
from Glastore.models.window import Window
from Glastore.models.window.position import WindowPositioner


def make_test_window(description):
    window = Window(
        product_id=1,
        description=description
    )
    window.add()

    return window


class WindowPositionerTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        descriptions = [
            "ventana fijo corrediza 10,10",
            "corrediza con dimenciones 10x10 y otra ventana",
            "fijos laterales de 10*10"
        ]
        #self.windows = []
        #for description in descriptions:
            #window = make_test_window(description)
            #self.windows.append(window)


class TestGetWindowPositions(WindowPositionerTest):

    def test_simple_window(self):
        window = make_test_window("ventana fija de 10,10")
        windows = [window]
        positioner = WindowPositioner(windows)
        window_positions = positioner.get_window_positions()
        self.assertEqual(window_positions, [[(0, 0)]])

    def test_simple_windows(self):
        window1 = make_test_window("ventana corrediza 10,10")
        window2 = make_test_window("fija con dimenciones 10x10 con texto extra")
        windows = [window1, window2]
        positioner = WindowPositioner(windows)
        window_positions = positioner.get_window_positions()
        self.assertEqual(window_positions[0], [(0, 0)])
        self.assertEqual(window_positions[1], [(10, 0)])

    def test_window_on_top(self):
        window1 = make_test_window("ventana corrediza 15,15")
        window2 = make_test_window("fijo superior con dimenciones 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(0, 0)])
        self.assertEqual(positions[1], [(0, 15)])

    def test_window_on_bottom(self):
        window1 = make_test_window("ventana corrediza 15,15")
        window2 = make_test_window("fijo inferior con dimenciones 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(0, 0)])
        self.assertEqual(positions[1], [(0, -10)])

    def test_window_twice(self):
        window = make_test_window("dos puertas abatibles de 15x15")
        positioner = WindowPositioner([window])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(0, 0), (15, 0)])

    def test_window_three_times(self):
        window = make_test_window("tres puertas abatibles de 15x15")
        positioner = WindowPositioner([window])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(0, 0), (15, 0), (30, 0)])

    def test_window_with_laterales(self):
        window1 = make_test_window("puerta abatible de 15x15")
        window2 = make_test_window("dos fijos laterales de 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(10, 0)])
        self.assertEqual(positions[1], [(25, 0), (0, 0)])

    def test_window_with_antepecho(self):
        window1 = make_test_window("puerta abatible de 15x15")
        window2 = make_test_window("antepecho fijo de 10x10")
        positioner = WindowPositioner([window1, window2])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(0, 0)])
        self.assertEqual(positions[1], [(0, 15)])

    def test_dos_laterales(self):
        window = make_test_window("puerta abatible de 10x15 con")
        laterales = make_test_window("dos fijos laterales de 5x15")
        positioner = WindowPositioner([window, laterales])
        positions = positioner.get_window_positions()
        self.assertEqual(positions[0], [(5, 0)])
        self.assertEqual(positions[1], [(15, 0), (0, 0)])


class TestEachMethod(WindowPositionerTest):

    def test_decide_window_position(self):
        window = make_test_window("puerta abatible de 10x15 con")
        superior = make_test_window("fijo superior de 5x15")
        positioner = WindowPositioner([window, superior])
        positioner.decide_window_position(superior)
        self.assertEqual(positioner.xposition, 0)
        self.assertEqual(positioner.yposition, window.height)

    def test_add_total_window_ocurrances(self):
        window = make_test_window("fijo de 5x15")
        puertas = make_test_window("dos puertas abatibles de 10x15")
        positioner = WindowPositioner([window, puertas])
        single_window = positioner.get_total_window_ocurrances(window)
        positioner.decide_window_position(puertas)
        double_window = positioner.get_total_window_ocurrances(puertas)
        self.assertEqual(single_window, [(0, 0)])
        self.assertEqual(double_window, [(5, 0), (15, 0)])

    def test_position_window_once(self):
        window = make_test_window("dos fijo de 5x15")
        positioner = WindowPositioner([window])
        positioner.total_window_ocurrances = []
        positioner.position_window_once()
        positioner.total_window_ocurrances = [(0, 0)]

    def test_handle_window_twice(self):
        puertas = make_test_window("dos puertas abatibles de 10x15")
        laterales = make_test_window("dos fijos laterales de 5x15")
        positioner = WindowPositioner([puertas, laterales])
        positioner.handle_laterales()
        positioner.total_window_ocurrances = []
        positioner.handle_window_twice(puertas)
        self.assertEqual(positioner.total_window_ocurrances, [(5, 0), (15, 0)])
        positioner.total_window_ocurrances = []
        positioner.handle_window_twice(laterales)
        self.assertEqual(positioner.total_window_ocurrances, [(15, 0), (0, 0)])


    def test_position_window_twice(self):
        puertas = make_test_window("puertas abatibles de 10x15")
        positioner = WindowPositioner([puertas])
        positioner.total_window_ocurrances = []
        positioner.position_window_twice(puertas)
        self.assertEqual(positioner.total_window_ocurrances, [(0, 0), (10, 0)])

    def test_handle_laterales(self):
        window = make_test_window("puerta abatible de 10x15 con")
        laterales = make_test_window("dos fijos laterales de 5x15")
        positioner = WindowPositioner([window, laterales])
        self.assertEqual(positioner.xposition, 0)
        positioner.handle_laterales()
        self.assertEqual(positioner.xposition, 5)

