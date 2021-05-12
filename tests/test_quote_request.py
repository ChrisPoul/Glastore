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
        data = dict(
            customer_name="Chris",
            email="test@email.com",
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, data):
            error = quote_request.edit()

        self.assertEqual(error, None)


class TestValidate(QuoteTest):

    def test_invalid_address(self):
        self.quote.address = ""
        error = self.quote.request.validate()

        self.assertNotEqual(error, None)


class TestValidateAddress(QuoteTest):

    def test_invalid_address(self):
        quote_request = QuoteRequest(self.quote)
        self.quote.address = ""
        error = quote_request.validate_address()

        self.assertNotEqual(error, None)


class TestValidateCustomer(QuoteTest):

    def test_name(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            customer_name="New Name"
        )
        with self.request_context(url, data):
            error = quote_request.validate_customer()

        self.assertNotEqual(error, None)


    def test_email(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            email="new@email.com"
        )
        with self.request_context(url, data):
            error = quote_request.validate_customer()

        self.assertNotEqual(error, None)


class TestValidateProducts(QuoteTest):

    def test_invalid_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name1="",
            material1="",
            acabado1="",
            cristal1=""
        )
        with self.request_context(url, data):
            error = quote_request.validate_products()

        self.assertNotEqual(error, None)

    def test_validate_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name1="",
            material1="",
            acabado1="",
            cristal1=""
        )
        with self.request_context(url, data):
            error = quote_request.validate_product(self.product)

        self.assertNotEqual(error, None)


class TestUpdate(QuoteTest):

    def test_pass(self):
        pass


class TestUpdateDate(QuoteTest):

    def test_update_date(self):
        quote_request = QuoteRequest(self.quote)
        old_date = self.quote.date
        quote_request.update_date()

        self.assertLess(old_date, self.quote.date)


class TestUpdateAddress(QuoteTest):

    def test_update_address(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            address="New Address"
        )
        with self.request_context(url, data):
            quote_request.update_address()

        self.assertEqual(self.quote.address, "New Address")


class TestUpgradeProducts(QuoteTest):

    def test_upgrade_products(self):
        pass


class TestAddProduct(QuoteTest):

    def test_add_existing_product(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        data = dict(
            name="Test"
        )
        with self.request_context(url, data):
            quote_request.add_product()

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
            quote_request.add_product()

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
            quote_request.add_product()

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
            quote_request.add_new_product()

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
            quote_request.add_product()

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
