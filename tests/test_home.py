from .setup import MyTest


class HomePage(MyTest):

    def test_home(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
