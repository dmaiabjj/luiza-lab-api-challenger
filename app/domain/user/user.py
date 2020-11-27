import enum

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from app import db
from app.domain import BaseModel


class RoleCategory(enum.Enum):
    SUPER_USER = 1
    CUSTOMER_EXPERIENCE = 2
    FINANCIAL = 3


# Define the Role Domain
class Role(db.Model, BaseModel):
    __tablename__ = 'roles'

    name = db.Column(db.String(512), nullable=False, server_default='')
    description = db.Column(db.Text, nullable=False, server_default='')
    category = db.Column(db.Enum(RoleCategory), default=RoleCategory.SUPER_USER)


# Define the User Role Domain
class UserRole(db.Model, BaseModel):
    __tablename__ = 'user_roles'
    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='_user_id_role_id'),)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# Define the User Domain
class User(db.Model, BaseModel):
    __tablename__ = 'users'
    serialize_rules = ('-password',)

    name = db.Column(db.String(512), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    roles = relationship(
        "UserRole",
        lazy='joined',
        uselist=False)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
