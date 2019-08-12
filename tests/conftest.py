# tests/conftest.py

import pytest
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.database import db
from app.cli import reset_db


@pytest.fixture(scope="session")
def global_data():
    return dict()


@pytest.fixture(scope="session")
def client():
    # setup
    test_app = create_app()

    from os import environ as env
    test_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite"
    test_app.config['TESTING'] = True
    client = test_app.test_client()

    with test_app.app_context():
        reset_db()
        create_admin("testadmin", "testadmin@mail.com", "testadmin")

    yield client

    # teardown
    with test_app.app_context():
        pass
        #drop_db()

def create_admin(username, email, password):
    from app.models.role import Role
    from app.models.user import User
    admin_role = Role()
    admin_role.name = "admin"
    admin_role.description = "the admin role duh."
    db.session.add(admin_role)
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.set_password(password)
    new_user.roles.append(admin_role)
    db.session.add(new_user) # update the user roles
    db.session.commit()