import os


class Config(object):
    DEBUG = False
    SECRET_KEY = 'secured_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_IMPORTS = ("tasks",)
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"]


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

