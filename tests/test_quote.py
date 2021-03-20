from .setup import MyTest
from .test_customer import make_test_customer
from Glastore.models import db, Quote


class AddQuote(MyTest):

    def test_add(self):
        make_test_customer()

        quote = Quote(customer_id=1)
        quote.add()
        assert quote in db.session

    def test_add_two(self):
        pass


class GetFolio(MyTest):

    def test_get_folio(self):
        quote = Quote()
        quote.add()
        self.assertEqual(quote.id, 1)
        self.assertEqual(quote.get_folio(), "G00001")


class GetTotals(MyTest):

    def test_get_totals(self):
        pass
