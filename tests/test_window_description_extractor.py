from .setup import MyTest
from Glastore.models.window.description import (
    WindowDescriptionExtractor, WindowIdentifierIndexExtractor,
    turn_dict_to_list
)


class TestGetWindowDescriptions(MyTest):

    def test_one_window_description(self):
        extractor = WindowDescriptionExtractor(
            "ventana fija de 10x10"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(
            window_descriptions, ["ventana fija de 10x10"]
        )
    
    def test_two_window_descriptions(self):
        extractor = WindowDescriptionExtractor(
            "ventana fija de 10x10 con abatible superior de 1.002x4.233"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(window_descriptions, [
            "ventana fija de 10x10 con ",
            "abatible superior de 1.002x4.233"
        ])

    def test_extended_window_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas fijas de 10x10"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(
            window_descriptions, ["dos ventanas fijas de 10x10", "fijas de 10x10"]
        )


class TestAddWindowDescription(MyTest):

    def test_fija(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "fija de 10x10"}
        )

    def test_dos_fijas(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "dos fijas de 10x10"}
        )

    def test_antepecho(self):
        extractor = WindowDescriptionExtractor("ventana antepecho de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "antepecho de 10x10"}
        )

    def test_antepecho_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho fijo de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "antepecho fijo de 10x10"}
        )

    def test_antepecho_y_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho y fijo de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "antepecho y "}
        )
        extractor.current_description_start = 20
        extractor.current_description_index = 1
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions,
            {0: "antepecho y ", 1: "fijo de 10x10"}
        )


class TestCurrentWindowDescription(MyTest):

    def test_fija(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        self.assertEqual(extractor.current_window_description, "fija de 10x10")

    def test_dos_fijas(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        self.assertEqual(extractor.current_window_description, "dos fijas de 10x10")

    def test_antepecho(self):
        extractor = WindowDescriptionExtractor("ventana antepecho de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        self.assertEqual(extractor.current_window_description, "antepecho de 10x10")

    def test_antepecho_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho fijo de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        self.assertEqual(extractor.current_window_description, "antepecho fijo de 10x10")

    def test_antepecho_y_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho y fijo de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        self.assertEqual(extractor.current_window_description, "antepecho y ")
        extractor.current_description_start = 20
        extractor.current_description_index = 1
        self.assertEqual(extractor.current_window_description, "fijo de 10x10")


class TestGetBasicWindowDescription(MyTest):

    def test_fija(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "fija de 10x10")

    def test_dos_fijas(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "dos ")
        extractor.current_description_start = 12
        extractor.current_description_index = 1
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "fijas de 10x10")

    def test_antepecho(self):
        extractor = WindowDescriptionExtractor("ventana antepecho de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "antepecho de 10x10")

    def test_antepecho_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho fijo de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "antepecho ")
        extractor.current_description_start = 18
        extractor.current_description_index = 1
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "fijo de 10x10")

    def test_antepecho_y_fijo(self):
        extractor = WindowDescriptionExtractor("ventana antepecho y fijo de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "antepecho y ")
        extractor.current_description_start = 20
        extractor.current_description_index = 1
        basic_description = extractor.get_basic_window_description()
        self.assertEqual(basic_description, "fijo de 10x10")


class TestHandleExtendedWindowDescription(MyTest):

    def test_dos_fijas(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.current_description_start = 0
        extractor.current_description_index = 0
        extractor.current_description = extractor.get_basic_window_description()
        self.assertEqual(extractor.current_description, "ventana dos ")
        extractor.handle_extended_window_description()
        self.assertEqual(extractor.current_description, "ventana dos fijas de 10x10")

    def test_antepecho_fijo(self):
        extractor = WindowDescriptionExtractor("ventana abatible antepecho fijo de 10x10")
        extractor.current_description_start = 17
        extractor.current_description_index = 1
        extractor.current_description = extractor.get_basic_window_description()
        self.assertEqual(extractor.current_description, "antepecho ")
        extractor.handle_extended_window_description()
        self.assertEqual(extractor.current_description, "antepecho fijo de 10x10")


class TestIsExtendedDescription(MyTest):

    def test_fija(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        self.assertEqual(extractor.is_extended_description("fija de 10x10"), False)

    def test_dos(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        self.assertEqual(extractor.is_extended_description("dos ventanas fijas"), True)

    def test_antepecho(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        self.assertEqual(extractor.is_extended_description("antepecho "), True)

    def test_antepecho_fijo(self):
        extractor = WindowDescriptionExtractor("ventana fija de 10x10")
        self.assertEqual(extractor.is_extended_description("antepecho fijo"), False)


class TestSaveWindowDescription(MyTest):

    def test_one_window_description(self):
        extractor = WindowDescriptionExtractor(
            "abatible de 10x10"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 0
        extractor.current_description_start = 0
        extractor.save_current_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "abatible de 10x10"}
        )

    def test_two_window_descriptions(self):
        extractor = WindowDescriptionExtractor(
            "corrediza de 2x2 con antepecho"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 0
        extractor.current_description_start = 0
        extractor.save_current_window_description()
        extractor.current_description_index = 1
        extractor.current_description_start = 21
        extractor.save_current_window_description()
        self.assertEqual(
            extractor.window_descriptions, 
            {0: "corrediza de 2x2 con ", 1: "antepecho"}
        )

    def test_two_part_window_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 0
        extractor.current_description_start = 0
        extractor.save_current_window_description()
        extractor.current_description_index = 1
        extractor.current_description_start = 13
        extractor.save_current_window_description()
        self.assertEqual(
            extractor.window_descriptions, {
                0: "dos ventanas abatibles de 10x10",
                1: "abatibles de 10x10"
            }
        )


class TestCurrentDescriptionIsPartOfAntepecho(MyTest):

    def test_some(self):
        pass

    
class TestIsLastDescription(MyTest):

    def test_last_window(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.current_description_index = 1
        self.assertEqual(extractor.is_last_description(), True)

    def test_not_last_window(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.current_description_index = 0
        self.assertEqual(extractor.is_last_description(), False)


class TestPreviousWindowDescription(MyTest):

    def test_previous_window_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.window_descriptions = {0: "dos ventanas "}
        extractor.current_description_index = 1
        self.assertEqual(extractor.previous_window_description, "dos ventanas ")

    def test_not_previous_window_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 1
        self.assertEqual(extractor.previous_window_description, "")


class TestExtendWindowDescription(MyTest):

    def test_extend_window_description(self):
        extractor = WindowDescriptionExtractor(
            "ventana abatible con fijas de 10x10"
        )
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.current_description = extractor.get_basic_window_description()
        self.assertEqual(extractor.current_description, "abatible con ")
        extractor.extend_window_description()
        self.assertEqual(
            extractor.current_description, "abatible con fijas de 10x10"
        )


class TestTurnDictToList(MyTest):

    def test_some_dict(self):
        some_dict = {
            1: "value1",
            2: "value2",
            3: "value3"
        }
        self.assertEqual(turn_dict_to_list(some_dict), ["value1", "value2", "value3"])
