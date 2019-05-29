from flask import Flask

from web import auth, api
from web.extensions import db, jwt, migrate, io


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('web')
    app.config.from_object('web.config')

    if testing is True:
        app.config['TESTING'] = True

    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
    io.init_app(app)
    migrate.init_app(app, db)
    # if cli is True:


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
