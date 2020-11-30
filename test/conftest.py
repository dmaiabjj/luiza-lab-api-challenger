import pytest
from sqlalchemy import MetaData

from app import create_app, db as database

# Initialize the Flask-App with test-specific settings
application = create_app(extra_config_settings=dict(
    TESTING=True,  # Propagate exceptions
    LOGIN_DISABLED=False,  # Enable @register_required
    SERVER_NAME='localhost',  # Enable url_for() without request context
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
))

# Setup an application context (since the tests run outside of the webserver context)
application.app_context().push()


@pytest.fixture(scope='session')
def app():
    """ Makes the 'app' parameter available to test functions. """
    return application


@pytest.fixture(scope='session')
def db():
    """ Makes the 'db' parameter available to test functions. """
    return database


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


def set_up(db):
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    for table in reversed(metadata.sorted_tables):
        db.session.execute(table.delete())
        db.session.commit()
    # Create and populate roles and users tables
    from app.commands.initialize_db import init_db

    init_db()
