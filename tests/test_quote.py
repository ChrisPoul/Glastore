from .setup import MyTest
from .test_customer import make_test_customer
from Glastore.models import (
    db, Quote, Customer, Product, format_date
)
from datetime import datetime


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
        date = datetime.now()
        quote.date = date
        error = quote.update()
        assert error is None
        assert quote.date == date


class DeleteQuote(MyTest):

    def test_delete(self):
        quote = Quote.new()
        assert quote in db.session
        quote.delete()
        assert quote not in db.session


class FolioAttribute(MyTest):

    def test_folio(self):
        quote = Quote.new()
        self.assertEqual(quote.id, 1)
        self.assertEqual(quote.folio, "G00001")


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


class AddProduct(MyTest):

    def test_add_product(self):
        customer = make_test_customer()
        product = Product(
            name="Test Product"
        )
        product.add()
        quote = Quote.new(customer.id)
        self.assertEqual(quote.sold_products, [])
        quote.add_product(product)
        self.assertEqual(quote.sold_products[0].product, product)


class EditProductView(MyTest):

    def test_view(self):
        customer = make_test_customer()
        Quote.new(customer.id)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertEqual(response.status_code, 200)

    def test_quote_info(self):
        customer = make_test_customer()
        quote = Quote.new(customer.id)
        response = self.client.get(
            'quote/edit/1'
        )
        formated_date = format_date(quote.date)
        self.assertIn(b"<img", response.data)
        self.assertIn(bytes(quote.folio, "utf-8"), response.data)
        self.assertIn(bytes(formated_date, "utf-8"), response.data)

    def test_customer_info(self):
        customer = Customer(
            name="Test Customer",
            email="test@email.com",
            address="Fake address"
        )
        customer.add()
        Quote.new(customer.id)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b"Test Customer", response.data)
        self.assertIn(b"test@email.com", response.data)
        self.assertIn(b"Fake address", response.data)

    def test_empty_product_inputs(self):
        customer = make_test_customer()
        Quote.new(customer.id)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'<input name="name"', response.data)
        self.assertIn(b'<input name="material"', response.data)
        self.assertIn(b'<input name="cristal"', response.data)
        self.assertIn(b'<input name="medidas"', response.data)

    def test_empty_product_values(self):
        customer = make_test_customer()
        Quote.new(customer.id)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'value="">', response.data)
        assert b'value="None">' not in response.data

    def test_add_product_function(self):
        customer = make_test_customer()
        product = Product(
            name="Test Product"
        )
        product.add()
        quote = Quote.new(customer.id)
        quote.add_product(product)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'Test Product', response.data)
        self.assertIn(b'<input name="material1"', response.data)
        self.assertIn(b'<input name="cristal1"', response.data)
        self.assertIn(b'<input name="medidas1"', response.data)

    def test_add_product_from_view(self):
        customer = make_test_customer()
        Quote.new(customer.id)
        product = Product(
            name="Test Product",
            material="Test Material",
            cristal="Test Cristal",
            medidas="1x1"
        )
        product.add()
        data = dict(
            name="Test Product"
        )
        response = self.client.post(
            'quote/edit/1',
            data=data
        )
        self.assertIn(b"Test Product", response.data)
        self.assertIn(b"Test Material", response.data)
        self.assertIn(b"Test Cristal", response.data)
        self.assertIn(b"1x1", response.data)
        self.assertIn(b'<input name="name"', response.data)

    def test_add_product_twice(self):
        customer = make_test_customer()
        Quote.new(customer.id)
        product = Product(
            name="Test Product",
            material="Test Material",
            cristal="Test Cristal",
            medidas="1x1"
        )
        product.add()
        data = dict(
            name="Test Product"
        )
        response = self.client.post(
            'quote/edit/1',
            data=data
        )
        new_response = self.client.post(
            'quote/edit/1',
            data=data
        )
        self.assertCountEqual(new_response.data, response.data)

    def test_update_products(self):
        customer = make_test_customer()
        quote = Quote.new(customer.id)
        product = Product(
            name="Test Product",
            material="Test Material",
            cristal="Test Cristal",
            medidas="1x1"
        )
        product.add()
        quote.add_product(product)
        data = dict(
            material1="New Material"
        )
        response = self.client.post(
            'quote/edit/1',
            data=data
        )
        self.assertIn(b"New Material", response.data)
