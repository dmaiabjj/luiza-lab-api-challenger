from flask import Blueprint, jsonify, request, make_response

from app.domain.customer.customer import Customer
from app.domain.customer.customer_repository import CustomerRepository
from app.presentation.base_custom_error import BaseCustomError, ErrorCode

customer_blueprint = Blueprint('customer', __name__, url_prefix='/api')
customer_repository = CustomerRepository()


@customer_blueprint.route('/customer', methods=['POST'])
def add():
    data = request.get_json()
    customer = {}
    customer = customer_repository.add(Customer(name=data['name'], email=data['email'], password=data['password']))
    return jsonify(customer)


@customer_blueprint.route('/customer/<id>', methods=['PUT'])
def update(id):
    customer = customer_repository.find_by_id(id=id)
    if customer is None:
        return make_response(jsonify(BaseCustomError(code=ErrorCode.ENTITY_NOT_FOUND.value,
                                                     message=ErrorCode.ENTITY_NOT_FOUND.name)), 404)
    return jsonify(customer)


@customer_blueprint.route('/customer/<id>/', methods=['GET'])
def get_by_id(id):
    customer = customer_repository.find_by_id(id=id)
    if customer is None:
        return make_response(jsonify(BaseCustomError(code=ErrorCode.ENTITY_NOT_FOUND.value,
                                                     message=ErrorCode.ENTITY_NOT_FOUND.name)), 404)
    return jsonify(customer)


@customer_blueprint.route('/customer/<offset>/<limit>', methods=['GET'])
def get_all(offset, limit):
    customers = customer_repository.get_all_by_paging(offset=offset, limit=limit)
    return jsonify(customers)
