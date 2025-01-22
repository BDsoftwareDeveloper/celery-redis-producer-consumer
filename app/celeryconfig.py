# # app/celeryconfig.py

# from celery import Celery

# # Create the Celery app instance
# app = Celery('pubsub_tasks', broker='redis://redis:6379/0')

# # Celery configuration
# app.conf.update(
#     result_backend='redis://redis:6379/0',
# )

from celery import Celery

# Initialize Celery app
app = Celery(
    'celery_app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)