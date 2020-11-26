from flask_user import UserMixin
from app import db
from app.domain.base_model import BaseModel


# Define the Customer data _domain
class Customer(BaseModel, UserMixin):
    __tablename__ = 'customers'
    name = db.Column(db.String(512), nullable=False, server_default='')
    # Required for Flask-User
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
