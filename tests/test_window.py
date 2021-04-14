from .setup import MyTest
from Glastore.models import db
from Glastore.models.window import Window


class WindowTest(MyTest):

    def test_add(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        self.assertIn(window, db.session)

    def test_remove(self):
        window = Window(
            product_id=1,
            description="a meaningless description"
        )
        window.add()
        self.assertIn(window, db.session)
        window.remove()
        self.assertNotIn(window, db.session)
