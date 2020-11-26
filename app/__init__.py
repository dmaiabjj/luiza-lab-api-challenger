from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

# Instantiate Flask extensions
db = SQLAlchemy()
migrate = Migrate()

from app.controllers.health_check import health_check_blueprint
from app.controllers.customer import customer_blueprint
from app.domain.customer.customer import Customer


def create_app(environment="local", settings=None):
    settings = settings or {}

    """Create a Flask app.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings from 'core/settings/base.py' file
    app.config.from_object('app.settings.base')
    # Load local settings from 'core/settings/local_settings.py'
    app.config.from_object(f'app.settings.{environment}_setting')
    # Load extra config settings from 'settings' param
    app.config.update(settings)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(customer_blueprint)

    UserManager(app, db, Customer)

    return app
