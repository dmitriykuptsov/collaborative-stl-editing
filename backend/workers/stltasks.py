from celery import Celery

celery = Celery(
    broker="redis://localhost:6379/0"
)

def send_task(file_path, object, version, owner):
    celery.send_task(
        "agents.tasks.process_stl",
        kwargs={
            "file_path": file_path,
            "object": object,
            "version": version,
            "owner": owner
        },
        queue="stl"#,
        #routing_key="stl"
    )
