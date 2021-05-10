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

    def test_add(self):
        quote = Quote(
            customer_id=1
        )
        quote.add()

        self.assertIn(quote, self.db.session)


class TestUpdate(QuoteTest):

    def test_update(self):
        self.quote.address = "Another address"
        self.quote.update()

        self.assertEqual(self.quote.address, "Another address")

    
class TestDelete(QuoteTest):

    def test_delete(self):
        self.quote.delete()

        self.assertNotIn(self.quote, self.db.session)
