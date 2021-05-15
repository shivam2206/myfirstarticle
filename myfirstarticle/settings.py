import os

# ---- Database configuration ----
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---- Flask App configuration  --------
APP_NAME = 'My First Article'
HOST = os.environ.get('APP_HOST', '127.0.0.1')
PORT = int(os.environ.get('APP_PORT', 5000))
SERVER_NAME = f'{HOST}:{PORT}'
SECRET_KEY = os.environ.get('SECRET_KEY', '\xfa\xa4\xf9c\x86\xbb\x1c\xaeK\x9cu\x99\xf4\xc3\xb3\x9e\xe1\x9e\x1c\xf5')
TOKEN_RETENTION_PERIOD_DAYS = 10

# ---- Swagger Configuration ----
APISPEC_SPEC = APISpec(
    title=APP_NAME,
    version='v1',
    plugins=[MarshmallowPlugin()],
    openapi_version='2.0.0'
),
APISPEC_SWAGGER_URL = '/swagger/'
APISPEC_SWAGGER_UI_URL = '/swagger-ui/'

MAX_PAGE_ITEMS = 20
