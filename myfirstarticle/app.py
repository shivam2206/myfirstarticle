from flask import Flask

from myfirstarticle import settings
from .database import db, migrate
from .model import *  # Do not remove this import


def create_app(config=None):
    """This function creates the Flask app and handles all the initial configuration"""
    app = Flask(settings.APP_NAME)
    app.config.from_object(settings)

    # Apply any modified config
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    return app
