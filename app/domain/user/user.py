import enum
from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

from app import db
from app.domain import BaseModel, Base


class RoleCategory(enum.Enum):
    ADMIN = 1
    SUPER_USER = 2
    CUSTOMER_EXPERIENCE = 3
    FINANCIAL = 4

    @classmethod
    def get_value(cls, member):
        return cls.__get_values().get(member)

    @classmethod
    def __get_values(cls):
        return {
            'ADMIN': RoleCategory.ADMIN,
            'SUPER_USER': RoleCategory.SUPER_USER,
            'CUSTOMER_EXPERIENCE': RoleCategory.CUSTOMER_EXPERIENCE,
            'FINANCIAL': RoleCategory.FINANCIAL
        }


# Define the User Role Domain
class UserRole(db.Model, Base, BaseModel):
    __tablename__ = 'roles'
    __table_args__ = (db.UniqueConstraint('user_id', 'category', name='_user_id_role_category'),)
    serialize_rules = ('-deleted_date', '-updated_date', '-user_id', '-id', '-created_date')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.Enum(RoleCategory), default=RoleCategory.ADMIN)


# Define the User Domain
class User(db.Model, Base, BaseModel):
    __tablename__ = 'users'
    serialize_rules = ('-password',)

    name = db.Column(db.String(512), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, server_default='', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    roles = relationship(
        "UserRole",
        lazy='joined')

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def change_roles(self, roles):
        self.updated_date = datetime.utcnow()
        all_roles = list(map(lambda role: role.category, self.roles))
        for r in roles:
            if r.category not in all_roles:
                self.roles.append(r)
