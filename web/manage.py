import os

import click
import sqlalchemy
from flask.cli import FlaskGroup

from app import create_app
from flask_migrate import upgrade


def create_web(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_web)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from web.extensions import db
    from web.models import User
    click.echo("create database")
    # 若数据库及数据库用户不存在则创建
    if os.getenv('FLASK_ENV') == 'development':
        engine = sqlalchemy.create_engine(os.getenv('DATABASE_INITIATE_URL'))  # connect to server
        engine.execute(
            'CREATE DATABASE IF NOT EXISTS zop default character set utf8 collate utf8_general_ci')  # create db
        # engine.execute('CREATE USER IF NOT EXISTS qcss IDENTIFIED BY "qmysql"')  # create user
        # engine.execute(sqlalchemy.text('GRANT ALL PRIVILEGES ON qcss.* TO "qcss"@"%"'))  # grand permission
        # engine.execute('FLUSH PRIVILEGES')  # flush permission
    # db.create_all()
    upgrade()
    click.echo("done")

    click.echo("create user")
    user = User(
        username='admin',
        email='admin@mail.com',
        password='admin',
        active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
