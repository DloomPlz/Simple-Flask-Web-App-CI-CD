# app/jwt.py

from os import environ as env
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)


def generate_jwt(claims, expiration=172800):
    s = Serializer(env.get("SECRET_KEY"), expires_in=expiration)
    return s.dumps(claims).decode("utf-8")


def load_jwt(token):
    s = Serializer(env.get("SECRET_KEY"))
    try:
        data = s.loads(token)
    except SignatureExpired as err:
        raise Exception(str(err))
    except BadSignature as err:
        raise Exception(str(err))
    return data
