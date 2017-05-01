import os

from extensions import db, migrate, celery
from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)


def create_manager_app(app=None):
    app = app or create_app()
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager
