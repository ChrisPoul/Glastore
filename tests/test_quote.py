from .setup import MyTest
from Glastore.models import db, Quote


class NewQuote(MyTest):

    def test_new(self):
        quote = Quote.new()
        self.assertIn(quote, db.session)
        self.assertEqual(quote.customer_id, 1)


class AddQuote(MyTest):

    def test_add(self):
        quote = Quote.new()
        assert quote in db.session

    def test_add_two_to_one_customer(self):
        quote = Quote.new()
        quote2 = Quote.new()
        assert quote in db.session
        assert quote2 in db.session

    def test_add_two_to_different_customers(self):
        quote = Quote.new()
        quote2 = Quote.new(customer_id=2)
        assert quote in db.session
        assert quote2 in db.session


class UpdateQuote(MyTest):

    def test_update(self):
        quote = Quote.new()
        quote.products = {1: 20}
        error = quote.update()
        assert error is None
        assert quote.products == {1: 20}


class DeleteQuote(MyTest):

    def test_delete(self):
        quote = Quote.new()
        assert quote in db.session
        quote.delete()
        assert quote not in db.session


class Attributes(MyTest):

    def test_folio(self):
        quote = Quote.new()
        self.assertEqual(quote.id, 1)
        self.assertEqual(quote.folio, "G00001")

    def test_totals(self):
        quote = Quote.new()
        quote.products = {1: 10, 2: 20}
        assert quote.totals == {1: 10, 2: 20}

    def test_total(self):
        quote = Quote.new()
        quote.products = {1: 10, 2: 10}
        self.assertEqual(quote.total, 20)


class GetQuote(MyTest):

    def test_get(self):
        quote = Quote.new()
        quote_search = Quote.get(1)
        self.assertEqual(quote_search, quote)

    def test_get_all(self):
        quote = Quote.new(customer_id=1)
        quote2 = Quote.new(customer_id=2)
        self.assertEqual(Quote.get_all(), [quote, quote2])

    def test_get_all_customer_quotes(self):
        quote = Quote.new(customer_id=1)
        quote2 = Quote.new(customer_id=1)
        Quote.new(customer_id=2)
        self.assertEqual(Quote.get_all(customer_id=1), [quote, quote2])
