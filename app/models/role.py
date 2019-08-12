# app/models/role.py

from .base import Base
from ..database import db


class Role(Base):

    __tablename__ = "roles"

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return self.name == other or self.name == getattr(other, "name", None)

    def __ne__(self, other):
        return not self.__eq__(other)
