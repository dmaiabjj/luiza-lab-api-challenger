from flask import current_app
from flask_script import Command

from app import db
from app.domain.customer.customer import Customer


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

    # Add customer
    find_or_create_user('Luke Skywalker', 'luke@luizalabs.com.br', 'darthVaderIsMyFather')
    # Save to DB
    db.session.commit()


def find_or_create_user(name, email, password):
    """ Find existing user or create new customer """
    user = Customer.query.filter(Customer.email == email).first()
    if not user:
        user = Customer(name=name, email=email,
                        password=current_app.user_manager.hash_password(password))

        db.session.add(user)
    return user
