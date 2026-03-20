# worker.py
from celery import Celery

celery = Celery(
    "stl_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
