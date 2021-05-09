from flask import Flask

from myfirstarticle import settings
from myfirstarticle.settings import APP_NAME


def create_app():
    """This function creates the Flask app and handles all the initial configuration"""
    flask_app = Flask(APP_NAME)
    flask_app.config.from_object(settings)
    return flask_app
