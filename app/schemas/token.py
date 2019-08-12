# app/schemas/token.py
# https://marshmallow.readthedocs.io/en/3.0/quickstart.html
# https://marshmallow.readthedocs.io/en/3.0/extending.html
# https://marshmallow.readthedocs.io/en/latest/nesting.html

from ..marshmallow import ma
from ..models.token import Token


class TokenSchema(ma.ModelSchema):
    class Meta:
        model = Token
        exclude = ["hash"]
        include_fk = True


token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)
