from flask_testing import TestCase
from Glastore.models import db
from Glastore import create_app


class MyTest(TestCase):

    def create_app(self):
        test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True
        }
        app = create_app(test_config)

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
