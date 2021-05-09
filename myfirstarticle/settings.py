import os

# ---- Database configuration ----
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']

# ---- Flask App configuration  --------
APP_NAME = 'My First Article'

# To enable debugging, export APP_ENV=debug
DEBUG = os.environ.get('APP_ENV') == 'debug'

HOST = int(os.environ.get('APP_HOST', '127.0.0.1'))
PORT = int(os.environ.get('APP_PORT', 5000))
