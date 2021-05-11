from .setup import MyTest
from flask import url_for
from Glastore.models.quote import Quote
from Glastore.models.customer import Customer
from Glastore.models.product import Product
from Glastore.models.quote.request import QuoteRequest


class QuoteTest(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.quote = Quote.new(1)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()
        self.product = Product(
            quote_id=1,
            name="Test",
            material="Material",
            acabado="Acabado",
            cristal="Cristal"
        )
        self.product.add()


class TestEdit(QuoteTest):

    def test_edit(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = {}
        with self.request_context(url, data):
            error = quote_request.edit()

        self.assertEqual(error, None)

    def test_date(self):
        quote_request = QuoteRequest(self.quote)
        old_date = self.quote.date
        url = url_for('quote.edit', id=self.quote.id)
        data = {}
        with self.request_context(url, data):
            error = quote_request.edit()

        self.assertEqual(error, None)
        self.assertLess(old_date, self.quote.date)

    def test_address(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = {}
        with self.request_context(url, data):
            error = quote_request.edit()

        self.assertEqual(error, None)
        self.assertEqual(self.quote.address, self.customer.address)

    
class TestValidate(QuoteTest):

    def test_address(self):
        self.quote.address = ""
        error = self.quote.request.validate()

        self.assertNotEqual(error, None)


class TestUpdateAddress(QuoteTest):

    def test_update_address(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            address="New Address"
        )
        with self.request_context(url, data):
            error = quote_request.update_address()

        self.assertEqual(error, None)
        self.assertEqual(self.quote.address, "New Address")


class TestUpdateCustomer(QuoteTest):

    def test_update_name(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            customer_name="New Name"
        )
        with self.request_context(url, data):
            error = quote_request.update_customer()

        self.assertEqual(error, None)
        self.assertEqual(self.customer.name, "New Name")


    def test_update_email(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            email="new@email.com"
        )
        with self.request_context(url, data):
            error = quote_request.update_customer()

        self.assertEqual(error, None)
        self.assertEqual(self.customer.email, "new@email.com")


class TestAddProduct(QuoteTest):

    def test_add_existing_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test"
        )
        with self.request_context(url, data):
            error = quote_request.add_product()

        self.assertEqual(error, None)
        self.assertEqual(len(self.quote.products), 2)

    def test_add_new_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, data):
            error = quote_request.add_product()

        self.assertEqual(error, None)
        self.assertEqual(len(self.quote.products), 2)

    def test_invalid_new_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test two",
            material="",
            acabado="",
            cristal=""
        )
        with self.request_context(url, data):
            error = quote_request.add_product()

        self.assertNotEqual(error, None)
        self.assertEqual(len(self.quote.products), 1)


class TestAddNewProduct(QuoteTest):

    def test_add_new_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, data):
            error = quote_request.add_new_product()

        self.assertEqual(error, None)
        self.assertEqual(len(self.quote.products), 2)
        self.assertEqual(self.quote.focused_product_id, 2)

    def test_invalid_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test two",
            material="",
            acabado="",
            cristal=""
        )
        with self.request_context(url, data):
            error = quote_request.add_product()

        self.assertNotEqual(error, None)
        self.assertEqual(len(self.quote.products), 1)
        self.assertEqual(self.quote.focused_product_id, 0)


class TestGetProduct(QuoteTest):

    def test_get_existing(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test"
        )
        with self.request_context(url, data):
            product = quote_request.get_product()

        self.assertEqual(product, self.product)

    def test_non_existing_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test two"
        )
        with self.request_context(url, data):
            product = quote_request.get_product()

        self.assertEqual(product, None)


class TestUpgradeProducts(QuoteTest):

    def test_upgrade_products(self):
        pass
