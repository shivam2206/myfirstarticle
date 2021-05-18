from myfirstarticle.database import db
from myfirstarticle.model import Author
from myfirstarticle.utils.helper import encode_auth_token, decode_auth_token
from tests.base import BaseTestCase


class TestAuthorModel(BaseTestCase):
    @staticmethod
    def create_author():
        author = Author(
            name='Sample User',
            email='user@sample.com',
            password='test123411'
        )
        return author

    def test_verify_password(self):
        author = self.create_author()
        assert not author.verify_password('invalid_password')
        assert author.verify_password('test123411')

    def test_password_readability(self):
        author = self.create_author()
        with self.assertRaises(AttributeError) as ae:
            password = author.password
        assert str(ae.exception) == 'Can\'t read password'

    def test_is_active(self):
        author = self.create_author()
        assert not author.is_active()

        author.active = True
        assert not author.is_active()

        author.active = False
        author.verified = True
        assert not author.is_active()

        author.active = True
        author.verified = True
        assert author.is_active()

    def test_get_id(self):
        author = self.create_author()
        assert author.get_id() == author.id
