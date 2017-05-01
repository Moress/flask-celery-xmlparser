from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class FlaskCelery(Celery):

    def __init__(self, *args, **kwargs):
        super(FlaskCelery, self).__init__(*args, **kwargs)

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def init_app(self, app):
        self.app = app
        app.config["BROKER_URL"] = app.config["CELERY_BROKER_URL"]
        self.config_from_object(app.config)

celery = FlaskCelery()
db = SQLAlchemy()
migrate = Migrate()

