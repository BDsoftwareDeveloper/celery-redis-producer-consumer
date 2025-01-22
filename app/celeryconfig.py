# app/celeryconfig.py

from celery import Celery

# Create the Celery app instance
app = Celery('pubsub_tasks', broker='redis://redis:6379/0')

# Celery configuration
app.conf.update(
    result_backend='redis://redis:6379/0',
)
