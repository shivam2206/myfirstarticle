from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_celeryext import FlaskCeleryExt
from flask_login import LoginManager
from flask_restful import Api

from myfirstarticle import settings
from .api.routes import initialize_routes
from .celery_utils import schedule_tasks
from .database import db, migrate
from .model import Author
from .utils.error_handler import handle_errors
from .home import home
from .articles import articles
from .authors import authors

ext_celery = FlaskCeleryExt()


def create_app(config=None):
    """This function creates the Flask app and handles all the initial configuration"""

    app = Flask(__name__)
    # Apply default config
    app.config.from_object(settings)
    if config:
        # Apply any modified config
        app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    ext_celery.init_app(app)
    schedule_tasks(ext_celery.celery)

    handle_errors(app)

    # Add Login Manager support
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "authors.login"

    @login_manager.user_loader
    def load_user(user_id):
        return Author.query.get(user_id)

    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(articles)
    app.register_blueprint(authors)

    # Add API support
    api = Api(app, prefix='/api/v1')
    docs = FlaskApiSpec(app)
    initialize_routes(api, docs)

    return app


