from werkzeug.security import check_password_hash

from app import db
from app.domain import BaseModel, Base


# Define the Customer Domain
class Customer(db.Model, Base, BaseModel):
    __tablename__ = 'customers'
    serialize_rules = ('-password',)

    name = db.Column(db.String(512), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
