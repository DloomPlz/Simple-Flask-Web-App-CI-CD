# app/models/base.py

import uuid
from .guid import GUID
from ..database import db


def generate_uuid():
    return str(uuid.uuid4())


class Base(db.Model):

    __abstract__ = True

    id = db.Column(GUID(), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
