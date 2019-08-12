# app/cli.py

import click
from flask.cli import with_appcontext
from .database import db
from .models.association import user_roles
from .models.role import Role
from .models.token import Token
from .models.user import User


@click.command("reset-db")
@with_appcontext
def reset_db_command():
    """Clear existing data and create new tables."""
    # run it with : FLASK_APP=. flask reset-db
    reset_db()
    click.echo("The database has been reset.")


def reset_db():
    db.drop_all()
    db.create_all()


@click.command("create-admin")
@click.argument("username")
@click.argument("email")
@click.argument("password")
@with_appcontext
def create_admin_command(username, email, password):
    # run it with : FLASK_APP=. flask create-admin 'XXX' 'YYY' 'ZZZ'
    admin_role = Role.query.filter(Role.name == "admin").first()
    if admin_role is None:
        admin_role = Role()
        admin_role.name = "admin"
        admin_role.description = "the admin role duh."
        db.session.add(admin_role)
        print(admin_role.id)
    click.echo("created: role 'admin'")
    if User.query.filter(User.username == username).first() is not None:
        return click.echo("username already taken")
    if User.query.filter(User.email == email).first() is not None:
        return click.echo("email already signed-up")
    new_user = User()
    new_user.username = username
    new_user.email = email
    new_user.set_password(password)
    new_user.roles.append(admin_role)
    db.session.add(new_user)  # update the user roles
    db.session.commit()
    return click.echo("created: user '" + username + " with 'admin' role")


def cli_init_app(app):
    app.cli.add_command(reset_db_command)
    app.cli.add_command(create_admin_command)
