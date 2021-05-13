from .setup import MyTest
from Glastore.models.quote import Quote


class QuoteTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.quote = Quote(
            customer_id=1,
            address="Test address"
        )
        self.quote.add()


class TestAdd(QuoteTest):

    def test_should_add_quote(self):
        quote = Quote(
            customer_id=1
        )
        quote.add()

        self.assertIn(quote, self.db.session)


class TestUpdate(QuoteTest):

    def test_should_update_quote(self):
        self.quote.address = "New address"
        self.quote.update()

        self.assertEqual(self.quote.address, "New address")

    
class TestDelete(QuoteTest):

    def test_should_delete_quote(self):
        self.quote.delete()

        self.assertNotIn(self.quote, self.db.session)
