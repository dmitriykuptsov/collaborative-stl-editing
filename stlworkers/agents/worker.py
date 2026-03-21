from celery import Celery

celery = Celery(
    "stl_worker",
    broker="redis://localhost:6379/0"
)

celery.conf.task_routes = {
    "tasks.process_stl": {"queue": "stl"},
}

