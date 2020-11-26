from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager


from .model.customer import Customer

# Instantiate Flask extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(environment="local", settings=None):
    settings = settings or {}

    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings from 'app/settings.py' file
    app.config.from_object('app.settings')
    # Load local settings from 'app/local_settings.py'
    app.config.from_object(f'app.{environment}_settings')

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    UserManager(app, db, Customer)

    return app
