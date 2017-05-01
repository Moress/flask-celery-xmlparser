from factory import create_app
from extensions import celery

create_app()

celery = celery
