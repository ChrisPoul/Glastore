from .setup import MyTest
from Glastore.models.product.final_window.description import SubWindowDescriptionIndexGetter


class TestGetWindowIdentifierIndexes(MyTest):

    def test_fija(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        self.assertEqual(extractor.get_window_description_indexes(), [0])

    def test_dos_abatibles(self):
        extractor = SubWindowDescriptionIndexGetter(
            "dos ventanas abatibles de 10x10"
        )
        self.assertEqual(extractor.get_window_description_indexes(), [0, 13])

    def test_antepecho_fijo(self):
        extractor = SubWindowDescriptionIndexGetter(
            "antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_window_description_indexes(), [0, 10])

    def test_dos_abatibles_con_antepecho_fijo(self):
        extractor = SubWindowDescriptionIndexGetter(
            "dos abatibles con antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_window_description_indexes(), [0, 4, 18, 28])

    def test_no_window_identified(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana de 10x10"
        )
        self.assertEqual(extractor.get_window_description_indexes(), [0])


class TestGetAllIdentifierIndexes(MyTest):

    def test_fija(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [8])

    def test_dos_abatibles(self):
        extractor = SubWindowDescriptionIndexGetter(
            "dos ventanas abatibles de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [0, 13])

    def test_antepecho_fijo(self):
        extractor = SubWindowDescriptionIndexGetter(
            "antepecho fijo de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [0, 10])

    def test_dos_abatibles_con_antepecho_fijo(self):
        extractor = SubWindowDescriptionIndexGetter(
            "dos abatibles con antepecho fijo de 10x10"
        )
        self.assertEqual(sorted(extractor.get_all_identifier_indexes()), [0, 4, 18, 28])

    def test_no_window_identified(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana de 10x10"
        )
        self.assertEqual(extractor.get_all_identifier_indexes(), [])


class TestAddIdentifierIndexes(MyTest):

    def test_add_some_indexes(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        extractor.all_identifier_indexes = []
        extractor.add_identifier_indexes([0, 8])
        self.assertEqual(extractor.all_identifier_indexes, [0, 8])


class TestGetIdentifierIndexes(MyTest):

    def test_fija(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        self.assertEqual(extractor.get_identifier_indexes("f"), [8])

    def test_dos(self):
        extractor = SubWindowDescriptionIndexGetter(
            "dos ventanas abatibles de 10x10"
        )
        self.assertEqual(extractor.get_identifier_indexes("dos"), [0])

    def test_two_identifier_instances(self):
        extractor = SubWindowDescriptionIndexGetter(
            "antepecho antepecho de 10x10"
        )
        self.assertEqual(extractor.get_identifier_indexes("antepecho"), [0, 10])

    def test_no_identifier_instance(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana de 10x10"
        )
        self.assertEqual(extractor.get_identifier_indexes("fijo"), [])
    

class TestGetIdentifierIndex(MyTest):

    def test_fija(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        extractor.start_of_search = 0
        self.assertEqual(extractor.get_identifier_index("fija"), 8)

    def test_no_result(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        extractor.start_of_search = 0
        self.assertEqual(extractor.get_identifier_index("abatible"), -1)


class TestAddIdentifierIndex(MyTest):

    def test_add_valid_index(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        extractor.current_identifier_indexes = []
        extractor.add_identifier_index(1)
        self.assertEqual(extractor.current_identifier_indexes, [1])

    def test_add_invalid_index(self):
        extractor = SubWindowDescriptionIndexGetter(
            "ventana fija de 10x10"
        )
        extractor.current_identifier_indexes = []
        extractor.add_identifier_index(-1)
        self.assertEqual(extractor.current_identifier_indexes, [])
