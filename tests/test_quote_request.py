from .setup import MyTest
from flask import url_for
from Glastore.models.quote import Quote
from Glastore.models.customer import Customer
from Glastore.models.product import Product
from Glastore.models.quote.request import QuoteRequest


class QuoteRequestTest(MyTest):

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


class TestEdit(QuoteRequestTest):

    def test_should_save_changes_given_valid_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            customer_name="Chris",
            email="test@email.com",
            address="New address",
            name1="New Name",
            material1="New Material",
            acabado1="New Acabado",
            cristal1="New Cristal",
            name="Test Two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, quote_data):
            quote_request.edit()
        self.db.session.rollback()

        self.assertEqual(self.customer.name, "Chris")
        self.assertEqual(self.product.name, "New Name")
        self.assertEqual(self.quote.address, "New address")
        self.assertEqual(len(Product.get_all()), 2)

    def test_should_not_save_changes_given_invalid_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            customer_name="",
            email="test.email.com",
            address="New address",
            name1="",
            material1="New Material",
            acabado1="",
            cristal1="New Cristal",
            name="Test Two",
            material="",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, quote_data):
            quote_request.edit()
        self.db.session.rollback()

        self.assertEqual(self.customer.name, "Test")
        self.assertEqual(self.product.name, "Test")
        self.assertNotEqual(self.quote.address, "New address")
        self.assertEqual(len(Product.get_all()), 1)


class TestDone(QuoteRequestTest):

    def test_should_create_new_sold_quote(self):
        self.assertEqual(len(self.quote.sold_quotes), 0)
        self.quote.request.done()
        self.assertEqual(len(self.quote.sold_quotes), 1)


class TestUpdateAttributes(QuoteRequestTest):

    def test_should_update_quote_given_valid_quote_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        old_date = self.quote.date
        with self.request_context(url, quote_data):
            quote_request.update_attributes()

        self.assertEqual(self.quote.address, "New Address")
        self.assertLess(old_date, self.quote.date)

    def test_should_update_quote_given_invalid_quote_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address=""
        )
        old_date = self.quote.date
        with self.request_context(url, quote_data):
            quote_request.update_attributes()

        self.assertEqual(self.quote.address, "")
        self.assertLess(old_date, self.quote.date)

    def test_should_not_save_changes(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        old_date = self.quote.date
        with self.request_context(url, quote_data):
            quote_request.update_attributes()
        self.db.session.rollback()

        self.assertNotEqual(self.quote.address, "New Address")
        self.assertEqual(old_date, self.quote.date)


class TestUpdateDate(QuoteRequestTest):

    def test_should_update_date(self):
        quote_request = QuoteRequest(self.quote)
        old_date = self.quote.date
        quote_request.update_date()

        self.assertLess(old_date, self.quote.date)

    def test_should_not_save_changes(self):
        quote_request = QuoteRequest(self.quote)
        old_date = self.quote.date
        quote_request.update_date()
        self.db.session.rollback()

        self.assertEqual(old_date, self.quote.date)


class TestUpdateAddress(QuoteRequestTest):

    def test_should_update_address(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        with self.request_context(url, quote_data):
            quote_request.update_address()

        self.assertEqual(self.quote.address, "New Address")

    def test_should_set_address_to_customer_address_given_no_address_has_been_set(self):
        quote_request = QuoteRequest(self.quote)
        quote_request.update_address()

        self.assertEqual(self.quote.address, self.customer.address)

    def test_should_not_save_changes(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        with self.request_context(url, quote_data):
            quote_request.update_address()
        self.db.session.rollback()

        self.assertNotEqual(self.quote.address, "New Address")


class TestAttemptUpdateAddress(QuoteRequestTest):

    def test_should_update_address(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        with self.request_context(url, quote_data):
            quote_request.attempt_update_address()

        self.assertEqual(self.quote.address, "New Address")

    def test_should_not_update_address_if_no_address_is_given(self):
        quote_request = QuoteRequest(self.quote)
        quote_request.attempt_update_address()

        self.assertEqual(self.quote.address, None)
    
    def test_should_not_save_changes(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        quote_data = dict(
            address="New Address"
        )
        with self.request_context(url, quote_data):
            quote_request.attempt_update_address()
        self.db.session.rollback()

        self.assertNotEqual(self.quote.address, "New Address")


class TestAddProduct(QuoteRequestTest):

    def test_should_duplicate_and_add_existing_product_given_product_name_exists(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test"
        )
        with self.request_context(url, product_data):
            quote_request.add_product()

        self.assertEqual(len(self.quote.products), 2)

    def test_should_create_and_add_new_product_given_valid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, product_data):
            quote_request.add_product()

        self.assertEqual(len(self.quote.products), 2)

    def test_should_not_create_and_add_new_product_given_invalid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two",
            material="",
            acabado="",
            cristal=""
        )
        with self.request_context(url, product_data):
            quote_request.add_product()

        self.assertEqual(len(self.quote.products), 1)


class TestAddNewProduct(QuoteRequestTest):

    def test_should_create_and_add_new_product_given_valid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, product_data):
            quote_request.add_new_product()

        self.assertEqual(len(self.quote.products), 2)
        self.assertEqual(self.quote.focused_product_id, 2)

    def test_should_not_create_and_add_new_product_given_invalid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two",
            material="",
            acabado="",
            cristal=""
        )
        with self.request_context(url, product_data):
            quote_request.add_new_product()

        self.assertEqual(len(self.quote.products), 1)
        self.assertEqual(self.quote.focused_product_id, 0)


class TestNewProduct(QuoteRequestTest):

    def test_should_return_new_product_given_valid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two",
            material="Material two",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        with self.request_context(url, product_data):
            product = quote_request.new_product

        self.assertEqual(product.name, "Test two")

    def test_should_return_new_product_given_invalid_product_data(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="",
            material="",
            acabado="",
            cristal=""
        )
        with self.request_context(url, product_data):
            product = quote_request.new_product

        self.assertEqual(product.name, "")


class TestMakeProduct(QuoteRequestTest):

    def test_should_return_product_created_using_form_data(self):
        quote_request = QuoteRequest(self.quote)
        form = dict(
            name="Test two",
            material="",
            acabado="Acabado two",
            cristal="Cristal two"
        )
        product = quote_request.make_product(form)

        self.assertEqual(product.name, "Test two")
        self.assertEqual(product.material, "")


class TestGetProduct(QuoteRequestTest):

    def test_should_return_product_given_existing_product_name(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test"
        )
        with self.request_context(url, product_data):
            product = quote_request.get_product()

        self.assertEqual(product, self.product)

    def test_should_return_none_given_non_existent_product_name(self):
        quote_request = QuoteRequest(self.quote)
        url = url_for('quote.edit', id=self.quote.id)
        product_data = dict(
            name="Test two"
        )
        with self.request_context(url, product_data):
            product = quote_request.get_product()

        self.assertEqual(product, None)
