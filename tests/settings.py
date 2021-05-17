
# ---- Database configuration ----
import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                      'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---- Flask App configuration  --------
APP_NAME = 'My First Article'
HOST = '127.0.0.1'
PORT = 5000
SERVER_NAME = f'{HOST}:{PORT}'
SECRET_KEY = 'SAMPLE SECRET KEY'
TOKEN_RETENTION_PERIOD_DAYS = 1

# ---- Swagger Configuration ----
APISPEC_TITLE = APP_NAME
APISPEC_SWAGGER_URL = '/swagger/'
APISPEC_SWAGGER_UI_URL = '/swagger-ui/'

MAX_PAGE_ITEMS = 2


ASSETS_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static/uploads')
