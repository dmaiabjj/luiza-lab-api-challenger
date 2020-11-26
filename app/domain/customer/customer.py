from flask_user import UserMixin
from app import db


# Define the Customer data domain
class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False, server_default='')
    # Required for Flask-User
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

