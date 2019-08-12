# app/api_v1/decorators.py

from functools import wraps
from flask import jsonify, request
from ..jwt import load_jwt
from ..models.user import User


def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify(err="no Authorization header found"), 400
        try:
            jwt = request.headers["Authorization"]
            claims = load_jwt(jwt)
        except Exception as err:
            return jsonify(err=str(err)), 401
        if "user_id" not in claims:
            return jsonify(err="token is not valid"), 400
        current_user = User.query.get(claims["user_id"])
        if current_user is None:
            return jsonify(err="404 User not found"), 400
        for token in current_user.tokens:
            if token.hash == jwt:
                token.current = True
                return fn(current_user=current_user, *args, **kwargs)
        return jsonify(err="token is not valid"), 401

    return wrapped


def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(current_user, *args, **kwargs):
            for required_role in roles:
                if current_user.has_role(required_role):
                    return fn(current_user=current_user, *args, **kwargs)
            return jsonify(err="you don't have the required roles"), 401

        return wrapped

    return wrapper
