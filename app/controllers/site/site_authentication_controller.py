from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.domain.customer.customer_repository import CustomerRepository
from app.domain.customer.customer_schema import CustomerAuthenticationInputSchema
from app.domain.customer.customer_service import CustomerService
from app.presentation.base_response_exception import BadRequestException

site_authentication_blueprint = Blueprint('site_authentication', __name__, url_prefix='/api')
customer_service = CustomerService(repository=CustomerRepository())


@site_authentication_blueprint.route('/auth/token', methods=['POST'])
def generate_token():
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


