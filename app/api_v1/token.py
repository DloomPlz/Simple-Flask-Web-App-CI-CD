# app/api_v1/token.py

from flask import jsonify
from . import api_v1_blueprint
from .decorators import login_required
from ..database import db
from ..schemas.token import tokens_schema


@api_v1_blueprint.route("/tokens", methods=["GET"])
@login_required
def list_tokens(current_user):
    json_tokens = tokens_schema.dump(current_user.tokens).data
    return jsonify(tokens=json_tokens)

@api_v1_blueprint.route("/tokens", methods=["DELETE"])
@login_required
def delete_all_tokens(current_user):
    for user_token in current_user.tokens:
        db.session.delete(user_token)
        db.session.commit()
    return jsonify(msg="you are now disconnected for every device"), 200


@api_v1_blueprint.route("/tokens/<token_id>", methods=["DELETE"])
@login_required
def delete_token(current_user, token_id):
    for user_token in current_user.tokens:
        if str(user_token.id) == token_id:
            db.session.delete(user_token)
            db.session.commit()
            return jsonify(msg="the token has been deleted"), 200
    return jsonify(err="404 token not found"), 404
