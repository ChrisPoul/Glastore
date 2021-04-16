from .setup import MyTest
from Glastore.models.window.description import WindowIdentifierIndexExtractor


class TestGetWindowIdentifierIndexes(MyTest):

    def test_fija(self):
        extractor = WindowIdentifierIndexExtractor(
            "ventana fija de 10x10"
        )
        self.assertEqual(extractor.get_window_identifier_indexes(), [8])

    def test_dos_abatibles(self):
        extractor = WindowIdentifierIndexExtractor(
            "dos ventanas abatibles de 10x10"
        )
        self.assertEqual(extractor.get_window_identifier_indexes(), [0, 13])

    def test_antepecho_fijo(self):
        extractor = WindowIdentifierIndexExtractor(
            "antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_window_identifier_indexes(), [0, 10])

    def test_dos_abatibles_con_antepecho_fijo(self):
        extractor = WindowIdentifierIndexExtractor(
            "dos abatibles con antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_window_identifier_indexes(), [0, 4, 18, 28])

    def test_no_window_identified(self):
        extractor = WindowIdentifierIndexExtractor(
            "ventana de 10x10"
        )
        self.assertEqual(extractor.get_window_identifier_indexes(), [0])


class TestGetAllIdentifierIndexes(MyTest):

    def test_fija(self):
        extractor = WindowIdentifierIndexExtractor(
            "ventana fija de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [8])

    def test_dos_abatibles(self):
        extractor = WindowIdentifierIndexExtractor(
            "dos ventanas abatibles de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [0, 13])

    def test_antepecho_fijo(self):
        extractor = WindowIdentifierIndexExtractor(
            "antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [0, 10])

    def test_dos_abatibles_con_antepecho_fijo(self):
        extractor = WindowIdentifierIndexExtractor(
            "dos abatibles con antepecho fijo de 10x10"
        )
        self.assertEqual(sorted(extractor.get_all_identifier_indexes()), [0, 4, 18, 28])

    def test_no_window_identified(self):
        extractor = WindowIdentifierIndexExtractor(
            "ventana de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [])
