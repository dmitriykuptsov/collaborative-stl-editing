# tasks.py
from worker import celery
import trimesh
import os

@celery.task(bind=True, max_retries=3)
def process_stl(self, file_path, model_id):
    try:
        mesh = trimesh.load(file_path)

        if not mesh.is_watertight:
            return {
                "status": "error",
                "reason": "Mesh is not watertight"
            }

        volume = mesh.volume
        bbox = mesh.bounding_box.extents.tolist()

        return {
            "status": "ok",
            "volume": volume,
            "bbox": bbox,
            "preview": preview_path
        }

    except Exception as e:
        raise self.retry(exc=e, countdown=10)
