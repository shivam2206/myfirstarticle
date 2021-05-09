import os


# ---- Database configuration ----
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ---- Flask App configuration  --------
APP_NAME = 'My First Article'
HOST = os.environ.get('APP_HOST', '127.0.0.1')
PORT = int(os.environ.get('APP_PORT', 5000))
SERVER_NAME = f'{HOST}:{PORT}'
