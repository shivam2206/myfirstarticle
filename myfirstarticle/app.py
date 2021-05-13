from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, jsonify
from flask_restful import Api

from myfirstarticle import settings
from .database import db, migrate
from .model import *  # Do not remove this import
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
    api = Api(app)

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='My First Article',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })
    docs = FlaskApiSpec(app)

    def add_route(resource, route):
        api.add_resource(resource, route)
        docs.register(resource)

    @app.errorhandler(422)
    def validation_error(err):
        messages = err.data.get('messages').get('json')
        response = {"status": "failed", "messages": messages}
        return jsonify(response), 422

    add_route(ArticleAPI, '/articles')

    return app
