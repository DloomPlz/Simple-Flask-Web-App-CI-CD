# app/models/user.py
# http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html

from .association import user_roles
from .base import Base
from .role import Role
from .token import Token
from ..bcrypt import bc
from ..database import db


class User(Base):

    __tablename__ = "users"

    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    encrypted_password = db.Column(db.String, nullable=False)

    roles = db.relationship(
        Role, secondary=user_roles, backref=db.backref("users", lazy="dynamic")
    )
    tokens = db.relationship(Token, backref="user")

    def has_role(self, role):
        if isinstance(role, str):
            # if role is the name of the role and not the object
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def set_password(self, password):
        self.encrypted_password = bc.generate_password_hash(password)

    def verify_password(self, password):
        return bc.check_password_hash(self.encrypted_password, password)
