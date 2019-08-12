# app/models/token.py

from .base import Base
from .guid import GUID
from ..database import db


class Token(Base):

    __tablename__ = "tokens"

    hash = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    user_id = db.Column(GUID(), db.ForeignKey("users.id"), nullable=False)
