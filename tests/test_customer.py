from .setup import MyTest
from Glastore.models.customer import Customer


class TestDbMethods(MyTest):

    def test_add(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer.add()

        self.assertIn(customer, self.db.session)
    
    def test_update(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer.add()
        customer.name = "New Test"
        customer.update()

        self.assertEqual(customer.name, "New Test")

    def test_delete(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer.add()
        customer.delete()
        
        self.assertNotIn(customer, self.db.session)

    
class TestQueryMethods(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    def test_get(self):
        customer = Customer.get(1)
        self.assertEqual(customer, self.customer)

    def test_get_all(self):
        customers = Customer.get_all()
        self.assertEqual(customers, [self.customer])


class TestSearchMethod(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    def test_with_name(self):
        customer = Customer.search("Test")
        self.assertEqual(customer, self.customer)

    def test_with_email(self):
        customer = Customer.search("test@email.com")
        self.assertEqual(customer, self.customer)

    def test_with_phone(self):
        customer = Customer.search("123 456 7890")
        self.assertEqual(customer, self.customer)

    def test_with_address(self):
        customer = Customer.search("Test address")
        self.assertEqual(customer, self.customer)

    def test_with_incorrect_search_term(self):
        customer = Customer.search("A wrong search term")
        self.assertEqual(customer, None)
