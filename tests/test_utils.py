from myfirstarticle.utils.helper import encode_auth_token, decode_auth_token
from tests.base import BaseTestCase


class TestUtils(BaseTestCase):
    def test_encode_auth_token(self):
        auth_token = encode_auth_token(234112)
        assert isinstance(auth_token, str)
        assert len(auth_token.split('.')) == 3

    def test_decode_auth_token(self):
        auth_token = encode_auth_token(5664422)
        assert decode_auth_token(auth_token) == 5664422
