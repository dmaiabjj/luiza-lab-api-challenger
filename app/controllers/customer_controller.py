from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from werkzeug.security import generate_password_hash

from app import blacklist
from app.domain.customer.customer import Customer
from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerInputSchema, CustomerUpdateInputSchema, \
    CustomerChangePasswordUpdateInputSchema
from app.domain.customer.customer_service import CustomerService
from app.helpers.auth_helper import super_user_required, admin_required
from app.presentation.base_response_exception import BadRequestException

customer_blueprint = Blueprint('customer', __name__, url_prefix='/api')
customer_service = CustomerService(repository=CustomerRepository())


def logout(jti):
    blacklist.add(jti)


@customer_blueprint.route('/customer', endpoint='add-customer', methods=['POST'])
def add_customer():
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


@customer_blueprint.route('/customer', endpoint='update_customer', methods=['PUT'])
@jwt_required
def update_customer():
    current_user = get_jwt_identity()
    customer_schema = CustomerUpdateInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    data['id'] = current_user['id']

    customer = customer_service.update(data)

    return jsonify(customer)


@customer_blueprint.route('/customer/<int:id>', endpoint='update_customer_by_id', methods=['PUT'])
@jwt_required
@super_user_required
def update_customer_by_id(id):
    customer_schema = CustomerUpdateInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    data['id'] = id

    customer = customer_service.update(data)

    return jsonify(customer)


@customer_blueprint.route('/customer', endpoint='delete_customer', methods=['DELETE'])
@jwt_required
def delete_customer():
    current_user = get_jwt_identity()
    customer_service.delete(id=current_user['id'])
    logout(get_raw_jwt()['jti'])
    return {}, 200


@customer_blueprint.route('/customer/<int:id>', endpoint='delete_customer_by_id', methods=['DELETE'])
@jwt_required
@super_user_required
def delete_customer_by_id(id):
    customer_service.delete(id=id)
    return {}, 200


@customer_blueprint.route('/customer/password', endpoint='change-customer-password', methods=['PUT'])
@jwt_required
def change_customer_password():
    current_user = get_jwt_identity()
    change_password_schema = CustomerChangePasswordUpdateInputSchema()
    data = request.get_json()

    errors = change_password_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Data", payload=errors)

    password = request.json.get('password', '')
    new_password = generate_password_hash(request.json.get('new_password', ''))

    customer_service.change_password(Customer(id=current_user['id'], password=new_password), password=password)

    return {}, 200


@customer_blueprint.route('/customer/<int:id>', endpoint='update-customer', methods=['PUT'])
@jwt_required
@admin_required
@super_user_required
def update_customer(id):
    customer_schema = CustomerUpdateInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    data['id'] = id

    customer = customer_service.update(data)

    return jsonify(customer)


@customer_blueprint.route('/customer/<int:id>', endpoint='delete-customer', methods=['DELETE'])
@jwt_required
@admin_required
@super_user_required
def delete_customer(id):
    customer_service.delete(id=id)
    return {}, 200


@customer_blueprint.route('/customer', endpoint='get-customer', methods=['GET'])
@jwt_required
def get_customer():
    current_user = get_jwt_identity()
    customer = customer_service.find_by_id(id=current_user['id'])
    return jsonify(customer)


@customer_blueprint.route('/customer/<int:id>', endpoint='get-customer-by-id', methods=['GET'])
@jwt_required
@admin_required
def get_customer_by_id(id):
    customer = customer_service.find_by_id(id=id)
    return jsonify(customer)


@customer_blueprint.route('/customer/email/<email>', endpoint='get-customer-by-email', methods=['GET'])
@jwt_required
@admin_required
def get_customer_by_email(email):
    customer = customer_service.find_by_email(email=email)
    return jsonify(customer)


@customer_blueprint.route('/customer/', endpoint='get-all-customers', methods=['GET'])
@customer_blueprint.route('/customer/<int:offset>/', endpoint='get-all-customers', methods=['GET'])
@customer_blueprint.route('/customer/<int:offset>/<int:limit>', endpoint='get-all-customers', methods=['GET'])
@jwt_required
@admin_required
def get_all_customers(offset=1, limit=10):
    customers = customer_service.get_all_paginated(offset=offset, limit=limit)
    return jsonify(customers)
