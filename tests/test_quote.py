from .setup import MyTest
from Glastore.models import db, Quote


def make_test_quote(customer_id=None, window_id=None):
    if not customer_id:
        customer_id = 1
    if not window_id:
        window_id = 1
    quote = Quote(
        customer_id=customer_id,
        products={window_id: 10}
    )
    quote.add()

    return quote


class AddQuote(MyTest):

    def test_add(self):
        quote = make_test_quote()
        assert quote in db.session

    def test_add_two_to_one_customer(self):
        quote = make_test_quote()
        quote2 = make_test_quote()
        assert quote in db.session
        assert quote2 in db.session

    def test_add_two_to_different_customers(self):
        quote = make_test_quote()
        quote2 = make_test_quote(customer_id=2)
        assert quote in db.session
        assert quote2 in db.session


class UpdateQuote(MyTest):

    def test_update(self):
        quote = make_test_quote()
        quote.products = {1: 20}
        error = quote.update()
        assert error is None
        assert quote.products == {1: 20}


class DeleteQuote(MyTest):

    def test_delete(self):
        quote = make_test_quote()
        assert quote in db.session
        quote.delete()
        assert quote not in db.session


class Attributes(MyTest):

    def test_folio(self):
        quote = make_test_quote()
        self.assertEqual(quote.id, 1)
        self.assertEqual(quote.folio, "G00001")

    def test_totals(self):
        quote = make_test_quote()
        quote.products = {1: 10, 2: 20}
        assert quote.totals == {1: 10, 2: 20}

    def test_total(self):
        quote = make_test_quote()
        quote.products = {1: 10, 2: 10}
        self.assertEqual(quote.total, 20)
