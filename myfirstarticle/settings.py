import os

# ---- Database configuration ----
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///application.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---- Flask App configuration  --------
APP_NAME = 'My First Article'
HOST = os.environ.get('APP_HOST', '127.0.0.1')
PORT = int(os.environ.get('APP_PORT', 5000))
# SERVER_NAME = f'{HOST}:{PORT}'
SECRET_KEY = os.environ.get('SECRET_KEY', '\xfa\xa4\xf9c\x86\xbb\x1c\xaeK\x9cu\x99\xf4\xc3\xb3\x9e\xe1\x9e\x1c\xf5')
TOKEN_RETENTION_PERIOD_DAYS = 10

# ---- Swagger Configuration ----
APISPEC_TITLE = APP_NAME
APISPEC_SWAGGER_URL = '/swagger/'
APISPEC_SWAGGER_UI_URL = '/swagger-ui/'

MAX_PAGE_ITEMS = 20


ASSETS_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static/uploads')


# ---- Celery Config ----
CELERY_BROKER_URL = os.environ.get('BROKER_URL', 'pyamqp://guest@localhost//')
