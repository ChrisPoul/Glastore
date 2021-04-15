from .setup import MyTest
from Glastore.models.window.description import WindowDescriptionExtractor, is_extended_description


class WindowDescriptionExtractorTest(MyTest):

    def test_make_basic_window_description(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        basic_description = extractor.make_basic_window_description()
        self.assertEqual(basic_description, "dos ")

    def test_handle_window_repetitions(self):
        extractor = WindowDescriptionExtractor("ventana dos fijas de 10x10")
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.current_description = extractor.make_basic_window_description()
        extractor.handle_window_repetitions()
        self.assertEqual(extractor.current_description, "dos fijas de 10x10")

    def test_extend_window_description(self):
        extractor = WindowDescriptionExtractor(
            "ventana abatible con fijas de 10x10"
        )
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.current_description = extractor.make_basic_window_description()
        extractor.extend_window_description()
        self.assertEqual(
            extractor.current_description, "abatible con fijas de 10x10"
        )

    def test_add_window_description(self):
        extractor = WindowDescriptionExtractor("ventana abatible de 10x10")
        extractor.window_descriptions = {}
        extractor.current_description_start = 8
        extractor.current_description_index = 0
        extractor.add_window_description()
        self.assertEqual(
            extractor.window_descriptions, {0: "abatible de 10x10"}
        )


class TestGetWindowDescriptions(MyTest):

    def test_one_window_description(self):
        extractor = WindowDescriptionExtractor(
            "ventana fija de 10x10"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(
            window_descriptions, ["fija de 10x10"]
        )
    
    def test_two_window_descriptions(self):
        extractor = WindowDescriptionExtractor(
            "ventana fija de 10x10 con abatible superior de 1.002x4.233"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(window_descriptions, [
            "fija de 10x10 con ",
            "abatible superior de 1.002x4.233"
        ])

    def test_extended_window_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas fijas de 10x10"
        )
        window_descriptions = extractor.get_window_descriptions()
        self.assertEqual(
            window_descriptions, ["dos ventanas fijas de 10x10"]
        )

class TestIsExtendedDescription(MyTest):

    def test_not_extended_window(self):
        self.assertEqual(is_extended_description("fija de 10x10"), False)

    def test_dos(self):
        self.assertEqual(is_extended_description("dos ventanas "), True)

    def test_antepecho(self):
        self.assertEqual(is_extended_description("antepecho "), True)


class SaveWindowDescriptionTest(MyTest):

    def test_one_window_description(self):
        extractor = WindowDescriptionExtractor(
            "ventana abatible de 10x10"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 0
        extractor.save_window_description("abatible de 10x10")
        self.assertEqual(
            extractor.window_descriptions, {0: "abatible de 10x10"}
        )

    def test_two_window_descriptions(self):
        extractor = WindowDescriptionExtractor(
            "ventana abatible de 10x10 con corrediza de 2x2"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 1
        extractor.save_window_description("corrediza de 2x2")
        self.assertEqual(
            extractor.window_descriptions, {1: "corrediza de 2x2"}
        )

    def test_two_part_description(self):
        extractor = WindowDescriptionExtractor(
            "dos ventanas abatibles de 10x10"
        )
        extractor.window_descriptions = {}
        extractor.current_description_index = 0
        extractor.save_window_description("dos ventanas abatibles de 10x10")
        extractor.current_description_index = 1
        extractor.save_window_description("abatibles de 10x10")
        self.assertEqual(
            extractor.window_descriptions, {
                0: "dos ventanas abatibles de 10x10"
            }
        )