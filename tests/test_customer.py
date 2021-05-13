from .setup import MyTest
from Glastore.models.customer import Customer


class TestAdd(MyTest):

    def test_should_add_customer(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer.add()

        self.assertIn(customer, self.db.session)
    

def TestUpdate(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    def test_should_update_customer(self):
        self.customer.name = "New Test"
        customer.update()
        self.db.session.rollback()

        self.assertEqual(self.customer.name, "New Test")


class TestDelete(MyTest):

    def test_should_delete_customer(self):
        customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        customer.add()
        customer.delete()
        
        self.assertNotIn(customer, self.db.session)

    
class TestGet(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    def test_should_return_customer_given_valid_id(self):
        customer = Customer.get(1)
        self.assertEqual(customer, self.customer)

    def test_should_return_none_given_invalid_id(self):
        customer = Customer.get(2)
        self.assertEqual(customer, None)


class TestGetAll(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()
        self.customer2 = Customer(
            name="Test 2",
            email="test2@email.com",
            phone="222 666 8888",
            address="Test address two"
        )
        self.customer2.add()

    def test_should_return_list_with_all_customers(self):
        customers = Customer.get_all()
        self.assertEqual(customers, [self.customer, self.customer2])


class TestSearch(MyTest):

    def setUp(self):
        MyTest.setUp(self)
        self.customer = Customer(
            name="Test",
            email="test@email.com",
            phone="123 456 7890",
            address="Test address"
        )
        self.customer.add()

    def test_should_return_customer_given_valid_name(self):
        customer = Customer.search("Test")
        self.assertEqual(customer, self.customer)

    def test_should_return_customer_given_valid_email(self):
        customer = Customer.search("test@email.com")
        self.assertEqual(customer, self.customer)

    def test_should_return_customer_given_valid_phone(self):
        customer = Customer.search("123 456 7890")
        self.assertEqual(customer, self.customer)

    def test_should_return_customer_given_valid_address(self):
        customer = Customer.search("Test address")
        self.assertEqual(customer, self.customer)

    def test_should_return_none_given_invalid_search_term(self):
        customer = Customer.search("A wrong search term")
        self.assertEqual(customer, None)
