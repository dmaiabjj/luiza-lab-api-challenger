from flask import jsonify

from app.controllers.site.site_authentication_controller import site_authentication_blueprint
from app.controllers.admin.admin_authentication_controller import admin_authentication_blueprint
from app.controllers.site.customer_controller import customer_blueprint
from app.controllers.admin.user_controller import user_blueprint
from ..presentation.base_response_exception import NotFoundException, BadRequestException, UnauthorizedException, \
    ResourceAlreadyExistsException, BaseResponseException


@customer_blueprint.errorhandler(NotFoundException)
@site_authentication_blueprint.errorhandler(NotFoundException)
@user_blueprint.errorhandler(NotFoundException)
@admin_authentication_blueprint.errorhandler(NotFoundException)
def handle_not_found(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(BadRequestException)
@site_authentication_blueprint.errorhandler(BadRequestException)
@user_blueprint.errorhandler(BadRequestException)
@admin_authentication_blueprint.errorhandler(BadRequestException)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(UnauthorizedException)
@site_authentication_blueprint.errorhandler(UnauthorizedException)
@user_blueprint.errorhandler(UnauthorizedException)
@admin_authentication_blueprint.errorhandler(UnauthorizedException)
def handle_unauthorized_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(ResourceAlreadyExistsException)
@site_authentication_blueprint.errorhandler(ResourceAlreadyExistsException)
@user_blueprint.errorhandler(ResourceAlreadyExistsException)
@admin_authentication_blueprint.errorhandler(ResourceAlreadyExistsException)
def handle_conflict_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@customer_blueprint.errorhandler(500)
@site_authentication_blueprint.errorhandler(500)
@user_blueprint.errorhandler(500)
@admin_authentication_blueprint.errorhandler(500)
def handle_server_error_request(error):
    response = jsonify(BaseResponseException(payload=error.message, message="An unexpected error happened sorry"))
    response.status_code = error.status_code
    return response


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['roles'] in 'SUPER_USER':
            return jsonify(msg='SUPER_USER only!'), 403
        else:
            return fn(*args, **kwargs)

    return wrapper
