# api_v1/__init__.py

from flask import Blueprint

root_blueprint = Blueprint("root", __name__)
api_v1_blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Import any endpoints here to make them available
from . import hello
from . import user
from . import token
from . import role
