# app/models/association.py
# http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html

from ..database import db
from .guid import GUID

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", GUID(), db.ForeignKey("users.id")),
    db.Column("role_id", GUID(), db.ForeignKey("roles.id")),
)
