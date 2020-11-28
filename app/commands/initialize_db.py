from werkzeug.security import generate_password_hash
from flask_script import Command
from sqlalchemy import and_

from app import db
from app.domain.customer.customer import Customer
from app.domain.user.user import User, UserRole, RoleCategory
from app.domain.wishlist.wishlist import WishList


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_customer()


def create_customer():
    """ Create users """

    # Create all tables
    db.create_all()

    # Add user
    user = find_or_create_user(name='Luke Skywalker', email='luke@luizalabs.com.br',
                               password='darthVaderIsMyFather')

    db.session.commit()

    # Add user role
    find_or_create_user_role(user_id=user.id, category=RoleCategory.ADMIN)
    find_or_create_user_role(user_id=user.id, category=RoleCategory.SUPER_USER)

    # Add customer
    customer = find_or_create_customer(name='Anakin Skywalker', email='anakin@starwars.com.br',
                                       password='iAmDarthVader')
    db.session.commit()

    # Add wishlist
    find_or_create_wishlist(customer_id=customer.id, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")

    # Save to DB
    db.session.commit()


def find_or_create_user(name, email, password):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).one_or_none()
    if not user:
        user = User(name=name, email=email,
                    password=generate_password_hash(password))

        db.session.add(user)
    return user


def find_or_create_user_role(user_id, category):
    """ Find existing user role or create new user role """
    user_role = UserRole.query.filter(and_(UserRole.user_id == user_id,
                                           UserRole.category == category)).one_or_none()
    if not user_role:
        user_role = UserRole(user_id=user_id, category=category)

        db.session.add(user_role)

    return user_role


def find_or_create_customer(name, email, password):
    """ Find existing customer or create new customer """
    customer = Customer.query.filter(Customer.email == email).one_or_none()
    if not customer:
        customer = Customer(name=name, email=email,
                            password=generate_password_hash(password))

        db.session.add(customer)
    return customer


def find_or_create_wishlist(customer_id, product_id):
    """ Find existing wishlist or create new wishlist """
    wishlist = WishList.query.filter(and_(WishList.customer_id == customer_id,
                                          WishList.product_id == product_id)).one_or_none()
    if not wishlist:
        wishlist = WishList(customer_id=customer_id, product_id=product_id)

        db.session.add(wishlist)

    return wishlist
