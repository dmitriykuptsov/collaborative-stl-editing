# tasks.py
from worker import celery
import trimesh
import numpy as np
import os
from models import session, ObjectVersions

@celery.task(bind=True, max_retries=3)
def process_stl(self, file_path, object, version):
    try:
        mesh = trimesh.load(file_path)
        volume = mesh.volume
        bbox = mesh.bounding_box.extents.tolist()
        surface_area = mesh.area
        num_facets = len(mesh.faces)
        unique_vertices = mesh.vertices
        edges = mesh.edges_unique
        counts = mesh.edges_unique_face_count
        non_manifold_edges = edges[counts != 2]
        is_edge_manifold = (mesh.edges_unique_face_count == 2).all()
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
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
