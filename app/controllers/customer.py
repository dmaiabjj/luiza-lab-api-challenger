from flask import Blueprint, jsonify, request, current_app

from app.domain.customer.customer import Customer
from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerInputSchema
from app.presentation.base_response_exception import NotFoundException, BadRequestException

customer_blueprint = Blueprint('customer', __name__, url_prefix='/api')
customer_repository = CustomerRepository()


@customer_blueprint.route('/customer', methods=['POST'])
def add():
    customer_schema = CustomerInputSchema()
    data = request.get_json()

    errors = customer_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Customer Data", payload=errors)

    customer = customer_repository.add(Customer(name=data['name'], email=data['email'],
                                                password=current_app.user_manager.hash_password(data['password'])))
    return jsonify(customer.to_dict())


@customer_blueprint.route('/customer/<id>', methods=['PUT'])
def update(id):
    customer = customer_repository.find_by_id(id=id)
    if customer is None:
        raise NotFoundException(message="Customer not found")
    return jsonify(customer.to_dict())


@customer_blueprint.route('/customer/<id>/', methods=['GET'])
def get_by_id(id):
    customer = customer_repository.find_by_id(id=id)
    if customer is None:
        raise NotFoundException(message="Customer not found")
    return jsonify(customer.to_dict())


@customer_blueprint.route('/customer/', methods=['GET'])
@customer_blueprint.route('/customer/<offset>/', methods=['GET'])
@customer_blueprint.route('/customer/<offset>/<limit>', methods=['GET'])
def get_all(offset=1, limit=10):
    customers = customer_repository.get_all_by_paging(offset=int(offset), limit=int(limit))
    return jsonify(list(map(lambda customer: customer.to_dict(), customers)))
