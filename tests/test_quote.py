from .setup import MyTest, make_test_customer
from Glastore.models import db, format_date
from Glastore.models.quote import Quote
from Glastore.models.product import Product
from datetime import datetime


class QuoteTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = make_test_customer()
        self.product = Product(
            quote_id=1,
            name="Test Product",
            material="Test Material",
            acabado="Test Acabado",
            cristal="Test Cristal",
            unit_price=10
        )
        self.product.add()
        self.quote = Quote.new(self.customer.id)


class NewQuote(QuoteTest):

    def test_new(self):
        quote = Quote.new()
        self.assertIn(quote, db.session)
        self.assertEqual(quote.customer_id, 1)


class AddQuote(QuoteTest):

    def test_add(self):
        quote = Quote.new()
        assert quote in db.session

    def test_add_two_to_one_customer(self):
        quote = Quote.new()
        quote2 = Quote.new()
        assert quote in db.session
        assert quote2 in db.session

    def test_add_two_to_different_customers(self):
        quote = Quote.new(customer_id=1)
        quote2 = Quote.new(customer_id=2)
        assert quote in db.session
        assert quote2 in db.session


class UpdateQuote(QuoteTest):

    def test_update(self):
        quote = Quote.new()
        date = datetime.now()
        quote.date = date
        error = quote.update()
        assert error is None
        assert quote.date == date


class DeleteQuote(QuoteTest):

    def test_delete(self):
        quote = Quote.new()
        assert quote in db.session
        quote.delete()
        assert quote not in db.session


class QuoteProperties(QuoteTest):

    def test_folio(self):
        quote = Quote.new()
        self.assertEqual(quote.id, 2)
        self.assertEqual(quote.folio, "G00002")

    def test_total(self):
        self.quote.add_product(self.product)
        self.quote.products[0].total = 20
        self.assertEqual(self.quote.total, 20)


class GetQuote(QuoteTest):

    def test_get(self):
        quote = Quote.new()
        quote_search = Quote.get(2)
        self.assertEqual(quote_search, quote)

    def test_get_all(self):
        quote = Quote.new(customer_id=1)
        quote2 = Quote.new(customer_id=2)
        self.assertEqual(Quote.get_all(), [self.quote, quote, quote2])

    def test_get_all_customer_quotes(self):
        quote2 = Quote.new(customer_id=1)
        quote3 = Quote.new(customer_id=2)
        self.assertEqual(Quote.get_all(customer_id=1), [self.quote, quote2])
        self.assertNotIn(quote3, Quote.get_all(customer_id=1))


class EditQuoteProducts(QuoteTest):

    def test_add_product(self):
        quote = Quote.new()
        quote.add_product(self.product)
        self.assertEqual(len(quote.products), 1)

    def test_add_product(self):
        quote = Quote.new()
        self.assertEqual(len(quote.products), 0)
        quote.add_product(self.product)
        self.assertEqual(len(self.quote.products), 1)
        quote.add_product(self.product)
        self.assertEqual(len(quote.products), 2)

    def test_add_duplicate_product(self):
        quote = Quote.new()
        quote.add_product(self.product)
        quote.add_product(self.product)
        self.assertEqual(len(quote.products), 2)
        self.assertNotEqual(Product.get(2), self.product)


class HandleSubmit(QuoteTest):

    def test_add_product(self):
        url = 'quote/edit/1'
        data = dict(
            name="Test Product"
        )
        with self.request_context(url, data):
            self.quote.request.add_product()
        self.assertIn(self.product, self.quote.products)

    def test_add_product_twice_on_submit(self):
        self.quote.add_product(self.product)
        url = 'quote/edit/1'
        data = dict(
            name="Test Product"
        )
        with self.request_context(url, data):
            self.quote.request.handle()
        self.assertEqual(self.quote.error, None)

    def test_add_new_product(self):
        quote = Quote.new()
        url = 'quote/edit/2'
        data = dict(
            name="A product",
            material="a material",
            acabado="un acabado",
            cristal="a material"
        )
        with self.request_context(url, data):
            quote.request.add_new_product()
        self.assertEqual(len(quote.products), 1)

    def test_add_empty_new_product_on_submit(self):
        quote = Quote.new()
        url = 'quote/edit/2'
        data = dict(
            name="A product",
            material="",
            cristal=""
        )
        with self.request_context(url, data):
            quote.request.add_new_product()
        self.assertEqual(len(quote.products), 0)

    def test_add_product_with_empty_acabado(self):
        quote = Quote.new()
        url = 'quote/edit/2'
        data = dict(
            name="A product",
            material="a material",
            acabado="",
            cristal="a cristal"
        )
        with self.request_context(url, data):
            quote.request.add_new_product()
        self.assertEqual(len(quote.products), 0)

    def test_new_product_empty_after_submit(self):
        url = 'quote/edit/1'
        data = dict(
            name="A product",
            material="",
            cristal=""
        )
        with self.request_context(url, data):
            self.quote.request.handle()
        self.assertEqual(self.quote.new_product.name, "")

    def test_add_duplicate_product_on_submit(self):
        quote = Quote.new()
        quote.add_product(self.product)
        url = 'quote/edit/2'
        data = dict(
            name="Test Product"
        )
        with self.request_context(url, data):
            quote.request.add_product()
        duplicate_product = Product.get(2)
        self.assertEqual(len(quote.products), 2)
        self.assertNotEqual(duplicate_product, self.product)

    def test_update_products(self):
        url = 'quote/edit/1'
        data = dict(
            material1="New Material",
            unit_price1=100,
            cantidad1=10,
            medidas1="2x2"
        )
        with self.request_context(url, data):
            self.quote.request.update_products()
            product = self.quote.products[0]
        self.assertEqual(product.material, "New Material")
        self.assertEqual(product.unit_price, 100.0)
        self.assertEqual(product.cantidad, 10)
        self.assertEqual(product.medidas, "2x2")

    def test_get_product(self):
        url = 'quote/edit/1'
        data = dict(
            name="Test Product"
        )
        with self.request_context(url, data):
            product = self.quote.request.get_product()
        self.assertEqual(product, self.product)

