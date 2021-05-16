from flask import Flask, render_template
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api

from myfirstarticle import settings
from .api.routes import initialize_routes
from .database import db, migrate
from .utils.error_handler import handle_errors
from .home import home
import os


def create_app(config=None):
    """This function creates the Flask app and handles all the initial configuration"""

    # TODO: Check why flask is not able to pick templates folder without specifying like below
    app = Flask(settings.APP_NAME,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static')
                )
    app.config.from_object(settings)

    # Apply any modified config
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    handle_errors(app)

    # Register blueprints
    app.register_blueprint(home)

    # Add API support
    api = Api(app, prefix='/api/v1')
    docs = FlaskApiSpec(app)
    initialize_routes(api, docs)

    return app
