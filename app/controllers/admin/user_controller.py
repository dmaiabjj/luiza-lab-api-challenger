from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_raw_jwt
from werkzeug.security import generate_password_hash

from app import blacklist
from app.controllers.admin import admin_required
from app.domain.user.user import User, UserRole
from app.domain.user.user_repository import UserRepository
from app.domain.user.user_schema import UserInputSchema, UserUpdateInputSchema, UserChangePasswordUpdateInputSchema
from app.domain.user.user_service import UserService
from app.presentation.base_response_exception import BadRequestException

user_admin_blueprint = Blueprint('user_admin', __name__, url_prefix='/admin/api')
user_service = UserService(repository=UserRepository())


def logout(jti):
    blacklist.add(jti)


@user_admin_blueprint.route('/user', methods=['POST'])
def add():
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


@user_admin_blueprint.route('/user', methods=['PUT'])
@jwt_required
@admin_required
def update():
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


@user_admin_blueprint.route('/user', methods=['DELETE'])
@jwt_required
@admin_required
def delete():
    current_user = get_jwt_identity()
    user_service.delete(id=current_user['id'])
    logout(get_raw_jwt()['jti'])

    return {}, 200


@user_admin_blueprint.route('/user/password', methods=['PUT'])
@jwt_required
@admin_required
def change_password():
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


@user_admin_blueprint.route('/user/<id>/', methods=['GET'])
@jwt_required
@admin_required
def get_by_id(id):
    user = user_service.find_by_id(id=int(id))
    return jsonify(user)


@user_admin_blueprint.route('/user/email/<email>/', methods=['GET'])
@jwt_required
@admin_required
def get_by_email(email):
    user = user_service.find_by_email(email=email)
    return jsonify(user)


@user_admin_blueprint.route('/user/', methods=['GET'])
@user_admin_blueprint.route('/user/<offset>/', methods=['GET'])
@user_admin_blueprint.route('/user/<offset>/<limit>', methods=['GET'])
@jwt_required
@admin_required
def get_all(offset=1, limit=10):
    users = user_service.get_all_paginated(offset=int(offset), limit=int(limit))
    return jsonify(users)
