from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.controllers.admin import admin_required, super_user_required
from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerUpdateInputSchema
from app.domain.customer.customer_service import CustomerService
from app.presentation.base_response_exception import BadRequestException

customer_admin_blueprint = Blueprint('customer_admin', __name__, url_prefix='/admin/api')
customer_service = CustomerService(repository=CustomerRepository())


@customer_admin_blueprint.route('/customer/<id>/', methods=['GET'])
@jwt_required
@admin_required
def get_by_id(id):
    customer = customer_service.find_by_id(id=int(id))
    return jsonify(customer)


@customer_admin_blueprint.route('/customer/email/<email>/', methods=['GET'])
@jwt_required
@admin_required
def get_by_email(email):
    customer = customer_service.find_by_email(email=email)
    return jsonify(customer)


@customer_admin_blueprint.route('/customer/', methods=['GET'])
@customer_admin_blueprint.route('/customer/<offset>/', methods=['GET'])
@customer_admin_blueprint.route('/customer/<offset>/<limit>', methods=['GET'])
@jwt_required
@admin_required
def get_all(offset=1, limit=10):
    customers = customer_service.get_all_paginated(offset=int(offset), limit=int(limit))
    return jsonify(customers)


@customer_admin_blueprint.route('/customer/<id>', methods=['PUT'])
@jwt_required
@admin_required
@super_user_required
def update(id):
    customer_schema = CustomerUpdateInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    data['id'] = int(id)

    customer = customer_service.update(data)

    return jsonify(customer)


@customer_admin_blueprint.route('/customer/<id>', methods=['DELETE'])
@jwt_required
@admin_required
@super_user_required
def delete(id):
    customer_service.delete(id=int(id))
    return {}, 200
