from flask_testing import TestCase
from myfirstarticle import create_app
from myfirstarticle.database import db
from tests import settings


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(config=settings)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

