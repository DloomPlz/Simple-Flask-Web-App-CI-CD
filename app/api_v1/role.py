# app/api_v1/role.py

from flask import jsonify, request
from . import api_v1_blueprint
from .decorators import login_required, roles_required
from ..database import db
from ..models.role import Role


@api_v1_blueprint.route("/roles", methods=["POST"])
@login_required
@roles_required("admin")
def route_roles_create(current_user):
    datas = request.get_json()
    name = datas.get("name", "")
    if name is "":
        return jsonify(error="name is empty"), 422
    # we could add some filters to our username
    description = datas.get("description", "")
    if description is "":
        return jsonify(error="description is empty"), 422
    if Role.query.filter(Role.name == name).first() is not None:
        return jsonify(err="role already exists"), 409
    new_role = Role()
    new_role.name = name
    new_role.description = description
    db.session.add(new_role)
    db.session.commit()
    return jsonify(msg="role successfully created"), 200


@api_v1_blueprint.route("/roles/<string:role_name>", methods=["DELETE"])
@login_required
@roles_required("admin")
def route_roles_delete(current_user, role_name):
    role = Role.query.filter(Role.name == role_name).first()
    if role is not None:
        db.session.delete(role)
        db.session.commit()
        return jsonify(msg="role was deleted"), 200
    return jsonify(err="role not found"), 200
