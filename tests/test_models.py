from .setup import MyTest
from Glastore.models import (
    add_to_db, Customer, db, commit_to_db,
    repeated_value_msg, get_form
)
from Glastore.customer import customer_heads


class CommitToDb(MyTest):

    def test_commit_to_db(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        db.session.add(customer)
        error = commit_to_db()
        assert error is None
        assert customer in db.session

    def test_repeated_value(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address"
        )
        db.session.add(customer)
        customer2 = Customer(
            name="Test",
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
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        error = add_to_db(customer)
        assert error is None
        assert customer in db.session

    def test_repeated_value(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            address="Fake address Apt. 12"
        )
        add_to_db(customer)
        customer2 = Customer(
            name="Test",
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
        with self.client:
            with self.app.test_request_context(
                    '/customer/update/1', data=data):
                form = get_form(customer_heads)

        self.assertEqual(form['name'], "Test")
        self.assertEqual(form['email'], "")
