from flask import Flask, render_template
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api

from myfirstarticle import settings
from .api.routes import initialize_routes
from .database import db, migrate
from .utils.error_handler import handle_errors
from .home import home
from .articles import articles


def create_app(config=None):
    """This function creates the Flask app and handles all the initial configuration"""

    app = Flask(__name__)
    app.config.from_object(settings)

    # Apply any modified config
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    handle_errors(app)

    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(articles)

    # Add API support
    api = Api(app, prefix='/api/v1')
    docs = FlaskApiSpec(app)
    initialize_routes(api, docs)

    return app
