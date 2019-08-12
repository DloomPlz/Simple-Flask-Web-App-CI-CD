# app/api_v1/user.py

import re
from flask import jsonify, request
from . import api_v1_blueprint
from .decorators import login_required, roles_required
from ..bcrypt import bc
from ..database import db
from ..jwt import generate_jwt
from ..models.role import Role
from ..models.token import Token
from ..models.user import User

@api_v1_blueprint.route("/signup", methods=["POST"])
def signup():
    datas = request.get_json()
    username = datas.get("username", "")
    if username is "":
        return jsonify(err="username is empty"), 422
    if not bool(re.match(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$", username)):
        return (
            jsonify(
                err="Username may only contain alphanumeric characters or single hyphens, and cannot begin or end with a hyphen"
            ),
            422,
        )
    email = datas.get("email", "")
    if email is "":
        return jsonify(err="email is empty"), 422
    # we could verify that this email is valid
    password = datas.get("password", "")
    if password is "":
        return jsonify(err="password is empty"), 422
    if User.query.filter(User.username == username).first() is not None:
        return jsonify(err="username already taken"), 409
    if User.query.filter(User.email == email).first() is not None:
        return jsonify(err="email already signed-up"), 409
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg="welcome :-)"), 200


@api_v1_blueprint.route("/login", methods=["POST"])
def login():
    datas = request.get_json()
    username = datas.get("username", "")
    if username is "":
        return jsonify(error="username is empty"), 422
    password = datas.get("password", "")
    if password is "":
        return jsonify(error="password is empty"), 422
    current_user = User.query.filter(User.username == username).first()
    if current_user is not None:
        if current_user.verify_password(password):
            claims = {"user_id": str(current_user.id)}
            jwt = generate_jwt(claims)
            token = Token()
            token.hash = jwt
            token.description = "could be location or something idk from request"
            token.user_id = current_user.id
            db.session.add(token)
            db.session.commit()
            return jsonify(token=jwt), 200
        return jsonify(err="password incorrect"), 401
    return jsonify(err="username incorrect"), 404


@api_v1_blueprint.route("/logout", methods=["POST"])
@login_required
def logout(current_user):
    for user_token in current_user.tokens:
        if user_token.hash == request.headers["Authorization"]:
            db.session.delete(user_token)
            db.session.commit()
            return jsonify(msg="logged out"), 200
    return jsonify(msg="logged out"), 200


@api_v1_blueprint.route(
    "/users/<string:username>/roles/<string:role_name>", methods=["POST"]
)
@login_required
@roles_required("admin")
def add_role_to_user(current_user, username, role_name):
    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify(error="user not found"), 404
    role = Role.query.filter(Role.name == role_name).first()
    if role is None:
        return jsonify(error="role not found"), 404
    if not user.has_role(role):
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
    return jsonify(msg="role has been successfully added to the user"), 200


@api_v1_blueprint.route(
    "/users/<string:username>/roles/<string:role_name>", methods=["DELETE"]
)
@login_required
@roles_required("admin")
def remove_role_from_user(current_user, username, role_name):
    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify(error="user not found"), 404
    role = Role.query.filter(Role.name == role_name).first()
    if role is None:
        return jsonify(error="role not found"), 404
    if user.has_role(role):
        user.roles.remove(role)
        db.session.add(user)
        db.session.commit()
    return jsonify(msg="role was removed from user"), 200
