from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

from app.domain.customer.customer import Customer
from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerInputSchema, CustomerUpdateInputSchema, \
    ChangePasswordUpdateInputSchema
from app.domain.customer.customer_service import CustomerService
from app.presentation.base_response_exception import BadRequestException

customer_blueprint = Blueprint('customer', __name__, url_prefix='/api')
customer_service = CustomerService(repository=CustomerRepository())


@customer_blueprint.route('/customer', methods=['POST'])
def add():
    customer_schema = CustomerInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    customer = customer_service.add(Customer(name=name, email=email, password=generate_password_hash(password)))

    return jsonify(customer)


@customer_blueprint.route('/customer', methods=['PUT'])
@jwt_required
def update():
    user_logged = get_jwt_identity()

    customer_schema = CustomerUpdateInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    email = request.json.get('email', None)
    name = request.json.get('name', None)

    customer = customer_service.update(Customer(id=int(user_logged['id']), name=name, email=email))

    return jsonify(customer)


@customer_blueprint.route('/customer', methods=['DELETE'])
@jwt_required
def delete():
    user_logged = get_jwt_identity()
    customer_service.delete(id=int(user_logged['id']))
    return {}, 200


@customer_blueprint.route('/customer/password', methods=['PUT'])
@jwt_required
def change_password():
    user_logged = get_jwt_identity()

    change_password_schema = ChangePasswordUpdateInputSchema()
    data = request.get_json()

    errors = change_password_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Data", payload=errors)

    password = request.json.get('password', '')
    new_password = generate_password_hash(request.json.get('new_password', ''))

    customer_service.change_password(Customer(id=int(user_logged['id']), password=new_password), password=password)

    return {}, 200


@customer_blueprint.route('/customer/<id>/', methods=['GET'])
@jwt_required
def get_by_id(id):
    customer = customer_service.find_by_id(id=int(id))
    return jsonify(customer)


@customer_blueprint.route('/customer/email/<email>/', methods=['GET'])
@jwt_required
def get_by_email(email):
    customer = customer_service.find_by_email(email=email)
    return jsonify(customer)


@customer_blueprint.route('/customer/', methods=['GET'])
@customer_blueprint.route('/customer/<offset>/', methods=['GET'])
@customer_blueprint.route('/customer/<offset>/<limit>', methods=['GET'])
@jwt_required
def get_all(offset=1, limit=10):
    customers = customer_service.get_all_paginated(offset=int(offset), limit=int(limit))
    return jsonify(customers)
