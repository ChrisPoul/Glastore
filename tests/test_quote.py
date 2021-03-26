from .setup import MyTest
from Glastore.models import db, format_date
from Glastore.models.quote import Quote, SoldProduct
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
        self.assertEqual(quote.id, 2)
        self.assertEqual(quote.folio, "G00002")


class GetQuote(MyTest):

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
        Quote.new(customer_id=2)
        self.assertEqual(Quote.get_all(customer_id=1), [self.quote, quote2])


class AddProduct(MyTest):

    def test_add_product(self):
        self.assertEqual(self.quote.sold_products, [])
        self.quote.add_product(self.product)
        self.assertEqual(self.quote.sold_products[0].product, self.product)


class EditProductView(MyTest):

    def test_view(self):
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertEqual(response.status_code, 200)

    def test_quote_info(self):
        response = self.client.get(
            'quote/edit/1'
        )
        formated_date = format_date(self.quote.date)
        self.assertIn(b"<img", response.data)
        self.assertIn(bytes(self.quote.folio, "utf-8"), response.data)
        self.assertIn(bytes(formated_date, "utf-8"), response.data)

    def test_customer_info(self):
        self.customer.name = "Test Customer"
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b"Test Customer", response.data)
        self.assertIn(b"Test@email.com", response.data)
        self.assertIn(b"Fake address", response.data)

    def test_empty_product_inputs(self):
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'<input name="name"', response.data)
        self.assertIn(b'<input name="material"', response.data)
        self.assertIn(b'<input name="cristal"', response.data)

    def test_empty_values(self):
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'value=""', response.data)
        assert b'value="None"' not in response.data

    def test_add_product_function(self):
        self.quote.add_product(self.product)
        response = self.client.get(
            'quote/edit/1'
        )
        self.assertIn(b'Test Product', response.data)
        self.assertIn(b'<input name="material1"', response.data)
        self.assertIn(b'<input name="cristal1"', response.data)
        self.assertIn(b'<input name="medidas1"', response.data)

    def test_add_product_from_view(self):
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
        self.assertIn(b'<input name="name"', response.data)

    def test_add_product_twice(self):
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
        self.assertNotEqual(new_response.data, response.data)

    def test_update_products(self):
        self.quote.add_product(self.product)
        data = dict(
            material1="New Material"
        )
        response = self.client.post(
            'quote/edit/1',
            data=data
        )
        self.assertIn(b"New Material", response.data)


class TestSoldProduct(MyTest):

    def test_add(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        error = sold_product.add()
        self.assertIn(sold_product, db.session)
        self.assertEqual(error, None)

    def test_update(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        sold_product.total = 1
        error = sold_product.update()
        self.assertEqual(error, None)
        self.assertEqual(sold_product.total, 1.0)

    def test_get(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        self.assertEqual(SoldProduct.get(1), sold_product)

    def test_edit_product_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            material1="New Material"
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_product_on_submit()
        self.assertEqual(self.product.material, "New Material")

    def test_edit_cantidad_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            cantidad1=1
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_cantidad_on_submit()
        self.assertEqual(sold_product.cantidad, str(1))

    def test_update_total(self):
        sold_product = SoldProduct(
            quote_id=1,
            product_id=1
        )
        sold_product.add()
        sold_product.cantidad = 1
        sold_product.update_total()
        self.assertEqual(sold_product.total, 10)

    def edit_on_submit(self):
        self.quote.add_product(self.product)
        sold_product = SoldProduct.get(1)
        data = dict(
            material1="Nuevo Material",
            cantidad1=1
        )
        url = 'quote/edit/1'
        with self.request_context(url, data):
            sold_product.edit_on_submit()
        self.assertEqual(self.product.material, "Nuevo Material")
        self.assertEqual(sold_product.cantidad, 1)
        self.assertEqual(sold_product.total, 10)
