from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.domain.user.user_schema import UserAuthenticationInputSchema
from app.domain.user.user_repository import UserRepository
from app.domain.user.user_service import UserService
from app.presentation.base_response_exception import BadRequestException

admin_authentication_blueprint = Blueprint('admin_authentication', __name__, url_prefix='/admin/api')
user_service = UserService(repository=UserRepository())


@admin_authentication_blueprint.route('/auth/token', methods=['POST'])
def generate_token():
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


