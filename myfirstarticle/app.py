from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask

from myfirstarticle import settings
from .database import db, migrate
from .model import *  # Do not remove this import
from .api import api
from flask_apispec.extension import FlaskApiSpec
from .api.routes.article import ArticleAPI


def create_app(config=None):
    """This function creates the Flask app and handles all the initial configuration"""
    app = Flask(settings.APP_NAME)
    app.config.from_object(settings)

    # Apply any modified config
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    # docs = FlaskApiSpec(app)
    # attach_routes(docs)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Awesome Project',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })
    docs = FlaskApiSpec(app)
    attach_routes(api, docs)
    return app


def attach_routes(_api, docs):
    _api.add_resource(ArticleAPI, '/articles')
    docs.register(ArticleAPI)
