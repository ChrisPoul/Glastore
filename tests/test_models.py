from .setup import MyTest
from Glastore.models import (
    add_to_db, db, commit_to_db,
    repeated_value_msg, get_form,
    format_price, format_date,
    add_comma_separators_to_num
)
from Glastore.models.customer import Customer
from Glastore.customer import customer_heads
from datetime import datetime


class CommitToDb(MyTest):

    def test_commit_to_db(self):
        customer = Customer(
            name="test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        db.session.add(customer)
        error = commit_to_db()
        assert error is None
        assert customer in db.session

    def test_repeated_value(self):
        customer = Customer(
            name="test",
            email="test@email.com",
            address="Fake address"
        )
        db.session.add(customer)
        customer2 = Customer(
            name="test",
            email="test@email.com",
            address="Fake address"
        )
        db.session.add(customer2)
        error = commit_to_db()
        assert error == repeated_value_msg
        assert customer not in db.session
        assert customer2 not in db.session


class AddToDb(MyTest):

    def test_add_to_db(self):
        customer = Customer(
            name="test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        error = add_to_db(customer)
        assert error is None
        assert customer in db.session

    def test_repeated_value(self):
        customer = Customer(
            name="test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        add_to_db(customer)
        customer2 = Customer(
            name="test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        error = add_to_db(customer2)
        assert error == repeated_value_msg
        assert customer in db.session
        assert customer2 not in db.session


class GetForm(MyTest):

    def test_get_form(self):
        data = {"name": "Test"}
        url = '/customer/update/1'
        with self.request_context(url, data):
            form = get_form(customer_heads)

        self.assertEqual(form['name'], "Test")
        self.assertEqual(form['email'], "")


class FormatFunctions(MyTest):

    def test_format_price(self):
        self.assertEqual(format_price(0), "$0.00")
        self.assertEqual(format_price(1), "$1.00")
        self.assertEqual(format_price(3.333), "$3.33")
        self.assertEqual(format_price(1000), "$1,000.00")
        self.assertEqual(format_price(1_000_000.8923), "$1,000,000.89")

    def test_format_date(self):
        date1 = datetime(2020, 1, 1, 1, 1)
        date2 = datetime(2020, 1, 2, 1, 1)
        self.assertEqual(format_date(date1), "Miércoles 01 de Enero del 2020")
        self.assertEqual(format_date(date2), "Jueves 02 de Enero del 2020")

    def test_add_comma_separators_to_num(self):
        self.assertEqual(add_comma_separators_to_num(1000), "1,000")
        self.assertEqual(add_comma_separators_to_num(1_000_000), "1,000,000")
