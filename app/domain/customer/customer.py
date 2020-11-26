from flask_user import UserMixin
from app import db
from app.domain import BaseModel


# Define the Customer Domain
class Customer(db.Model, BaseModel, UserMixin):
    __tablename__ = 'customers'
    serialize_rules = ('-password',)

    name = db.Column(db.String(512), nullable=False, server_default='')
    # Required for Flask-User
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
