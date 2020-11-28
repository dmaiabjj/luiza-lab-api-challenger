from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_raw_jwt
from werkzeug.security import generate_password_hash

from app import blacklist
from app.domain.user.user import User, UserRole
from app.domain.user.user_repository import UserRepository
from app.domain.user.user_schema import UserInputSchema, UserUpdateInputSchema, UserChangePasswordUpdateInputSchema
from app.domain.user.user_service import UserService
from app.helpers.auth_helper import admin_required
from app.presentation.base_response_exception import BadRequestException

user_blueprint = Blueprint('user', __name__, url_prefix='/api')
user_service = UserService(repository=UserRepository())


def logout(jti):
    blacklist.add(jti)


@user_blueprint.route('/user', endpoint='add-user', methods=['POST'])
@jwt_required
@admin_required
def add_user():
    user_schema = UserInputSchema()
    data = request.get_json()

    errors = user_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid User Data", payload=errors)

    name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    roles = list(map(lambda category: UserRole(category=category), request.json.get('roles', [])))

    user = user_service.add(User(name=name, email=email, password=generate_password_hash(password), roles=roles))

    return jsonify(user)


@user_blueprint.route('/user', endpoint='update-user', methods=['PUT'])
@jwt_required
@admin_required
def update_user():
    current_user = get_jwt_identity()
    user_schema = UserUpdateInputSchema()
    data = request.get_json()

    errors = user_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid User Data", payload=errors)

    data['id'] = current_user['id']
    roles = request.json.get('roles', [])

    user = user_service.update(data, roles)

    return jsonify(user)


@user_blueprint.route('/user', endpoint='delete-user', methods=['DELETE'])
@jwt_required
@admin_required
def delete_user():
    current_user = get_jwt_identity()
    user_service.delete(id=current_user['id'])
    logout(get_raw_jwt()['jti'])

    return {}, 200


@user_blueprint.route('/user/password', endpoint='change-user-password', methods=['PUT'])
@jwt_required
@admin_required
def change_user_password():
    current_user = get_jwt_identity()
    change_password_schema = UserChangePasswordUpdateInputSchema()
    data = request.get_json()

    errors = change_password_schema.validate(data)
    if errors:
        raise BadRequestException(message="Invalid Data", payload=errors)

    password = request.json.get('password', '')
    new_password = generate_password_hash(request.json.get('new_password', ''))

    user_service.change_password(User(id=current_user['id'], password=new_password), password=password)

    return {}, 200


@user_blueprint.route('/user', endpoint='get-user', methods=['GET'])
@jwt_required
@admin_required
def get_user():
    current_user = get_jwt_identity()
    user = user_service.find_by_id(id=current_user['id'])
    return jsonify(user)


@user_blueprint.route('/user/<int:id>', endpoint='get-user-by-id', methods=['GET'])
@jwt_required
@admin_required
def get_user_by_id(id):
    user = user_service.find_by_id(id=id)
    return jsonify(user)


@user_blueprint.route('/user/email/<email>/', endpoint='get-user-by-email', methods=['GET'])
@jwt_required
@admin_required
def get_user_by_email(email):
    user = user_service.find_by_email(email=email)
    return jsonify(user)


@user_blueprint.route('/user/', endpoint='get-all-users', methods=['GET'])
@user_blueprint.route('/user/<int:offset>/', endpoint='get-all-users', methods=['GET'])
@user_blueprint.route('/user/<int:offset>/<int:limit>', endpoint='get-all-users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users(offset=1, limit=10):
    users = user_service.get_all_paginated(offset=offset, limit=limit)
    return jsonify(users)
