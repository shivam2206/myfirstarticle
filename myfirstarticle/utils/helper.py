from datetime import datetime, timedelta

import jwt

from myfirstarticle.settings import SECRET_KEY, TOKEN_RETENTION_PERIOD_DAYS


def encode_auth_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=TOKEN_RETENTION_PERIOD_DAYS),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired. Please log in again.')
    except jwt.InvalidTokenError as e:
        raise Exception('Invalid token. Please log in again.')
