from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager
)

# Instantiate Flask extensions
db = SQLAlchemy()
migrate = Migrate()
blacklist = set()

from app.controllers.authentication_controller import authentication_blueprint
from app.controllers.customer_controller import customer_blueprint
from app.controllers.product_controller import product_blueprint
from app.controllers.user_controller import user_blueprint
from app.controllers.wishlist_controller import wishlist_blueprint
from app.controllers.health_check_controller import health_check_blueprint

from app.domain.customer.customer import Customer


def create_app(extra_config_settings={}):

    """Create a Flask app.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings from 'core/settings/base.py' file
    app.config.from_object('app.settings.base')
    app.config.from_object(f'app.settings.local_setting')
    # Load extra config settings from 'settings' param
    app.config.update(extra_config_settings)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Register blueprints

    # General blueprint
    app.register_blueprint(health_check_blueprint)
    # Domain blueprint
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(wishlist_blueprint)

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        if 'roles' in user:
            return {'roles': list(map(lambda role: role['category'], user['roles']))}
        else:
            return {'roles': []}

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    return app
