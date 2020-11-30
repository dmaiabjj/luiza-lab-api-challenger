# *****************************
# Local environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
import os

DEBUG = True
SECRET_KEY = 'This is an UNSECURE Secret. CHANGE THIS for production environments.'

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
database_url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_user,
                                                       db_password,
                                                       db_host,
                                                       db_port,
                                                       db_name)

# SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_TYPE = 'sqlalchemy'
