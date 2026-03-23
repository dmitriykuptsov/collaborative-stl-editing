import trimesh
import numpy as np
import os
from models.models import session, ObjectVersions

from datetime import datetime, timedelta

from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)

celery.conf.task_routes = {
    "tasks.process_stl": {"queue": "stl"},
}

@celery.task(bind=True, max_retries=3)
def process_stl(self, file_path, object, version, owner):
    try:
        mesh = trimesh.load(file_path)
        volume = mesh.volume
        bbox = mesh.bounding_box.extents.tolist()
        surface_area = mesh.area
        num_facets = len(mesh.faces)
        unique_vertices = mesh.vertices
        edges = mesh.edges_unique
        #counts = mesh.edges_unique_face_count
        #non_manifold_edges = edges[counts != 2]
        #is_edge_manifold = (mesh.edges_unique_face_count == 2).all()
        is_watertight = mesh.is_watertight
        non_manifold_vertices = []
        for v_idx in range(len(mesh.vertices)):
            faces = mesh.vertex_faces[v_idx]
            faces = faces[faces != -1]
            if len(faces) == 0:
                continue
            submesh = mesh.submesh([faces], append=True)
            if len(submesh.split()) > 1:
                non_manifold_vertices.append(v_idx)
        is_vertex_manifold = len(non_manifold_vertices) == 0
        cog = mesh.center_mass
        cog_x = cog[0]
        cog_y = cog[1]
        cog_z = cog[2]

        obj = session.query(ObjectVersions).filter_by(object = object, version = version, owner = owner).first()
        if not obj:
            return
        obj.surface_area = surface_area
        obj.volume = volume
        obj.cog_x = cog_x
        obj.cog_y = cog_y
        obj.cog_z = cog_z
        obj.bb_x_l = bbox[0]
        obj.bb_y_l = bbox[1]
        obj.bb_z_l = bbox[2]
        obj.is_water_tight = is_watertight
        obj.number_of_facets = num_facets
        obj.number_of_unique_edges = len(edges)
        obj.number_of_unique_verticies = len(unique_vertices)
        #obj.is_edge_manifold = is_edge_manifold
        obj.is_vertex_manifold = is_vertex_manifold
        obj.date_uploaded = datetime.now();

        session.commit();
    
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
