from functools import wraps

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_claims
)

from app.presentation.base_response_exception import UnauthorizedException


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'ADMIN' in claims['roles']:
            return fn(*args, **kwargs)
        else:
            raise UnauthorizedException(message="SUPER_USER only")

    return wrapper


def super_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if 'SUPER_USER' in claims['roles']:
            return fn(*args, **kwargs)
        else:
            raise UnauthorizedException(message="SUPER_USER only")

    return wrapper
