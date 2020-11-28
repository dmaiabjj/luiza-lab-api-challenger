from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerAuthenticationInputSchema
from app.domain.customer.customer_service import CustomerService
from app.domain.user.user_schema import UserAuthenticationInputSchema
from app.domain.user.user_repository import UserRepository
from app.domain.user.user_service import UserService
from app.presentation.base_response_exception import BadRequestException

authentication_blueprint = Blueprint('authentication', __name__, url_prefix='/api')
user_service = UserService(repository=UserRepository())
customer_service = CustomerService(repository=CustomerRepository())


@authentication_blueprint.route('/auth/user/token', endpoint='generate-user', methods=['POST'])
def generate_user_token():
    authentication_schema = UserAuthenticationInputSchema()
    data = request.get_json()

    errors = authentication_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Authentication Data", payload=errors)

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = user_service.login(email=email, password=password)

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@authentication_blueprint.route('/auth/customer/token', endpoint='generate-customer', methods=['POST'])
def generate_customer_token():
    authentication_schema = CustomerAuthenticationInputSchema()
    data = request.get_json()

    errors = authentication_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Authentication Data", payload=errors)

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    customer = customer_service.login(email=email, password=password)

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=customer)
    return jsonify(access_token=access_token)
