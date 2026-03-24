from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response, send_file, Response
import os
from binascii import hexlify
import app
from app import db
from app import config_
from models.models import Users
from models.models import Objects
from models.models import ObjectVersions
from datetime import datetime
import secrets
import re
from datetime import tzinfo, timezone
from utils.utils import get_subject, is_valid_session, hash_string
from workers import stltasks

mod_upload = Blueprint('upload', __name__, url_prefix='/upload')

@mod_upload.route("/create_object_description/", methods=["POST"])
def create_object_description():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = get_subject(request, config_)
    object = Objects.query.filter(db.and_(Objects.object == data.get("name"), Objects.owner == username)).first()
    if object:
        return jsonify({
            "success": False,
            "reason": "Объект уже существует"
        })
    
    object = Objects()
    object.object = data.get("name")
    object.description = data.get("description")
    object.owner = username
    object.creation_time = datetime.now(tz=timezone.utc)

    db.session.add(object)
    db.session.commit()
    
    return jsonify({
        "success": True
    })

@mod_upload.route("/get_objects/", methods=["POST"])
def get_objects():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    
    offset = data.get("offset")
    limit = data.get("limit", 10)

    username = get_subject(request, config_)
    objects = Objects.query.filter(db.and_(Objects.owner == username)).offset(offset=offset).limit(limit).all()

    result = []

    for _ in objects:
        result.append({
            "name": _.object,
            "creation_date": _.creation_time,
            "owner": _.owner
        })
    
    return jsonify({
        "success": True,
        "result": result
    })

@mod_upload.route("/get_objects_count/", methods=["POST"])
def get_objects_count():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })    

    username = get_subject(request, config_)
    _ = Objects.query.filter(db.and_(Objects.owner == username)).count()
    
    return jsonify({
        "success": True,
        "result": _
    })

@mod_upload.route("/get_versions_count/", methods=["POST"])
def get_versions_count():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })

    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    object = data.get("name")
    

    username = get_subject(request, config_)
    _ = ObjectVersions.query.filter(db.and_(ObjectVersions.owner == username, ObjectVersions.object == object)).count()
    
    return jsonify({
        "success": True,
        "result": _
    })

@mod_upload.route("/get_versions/", methods=["POST"])
def get_versions():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })

    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    offset = data.get("offset")
    limit = data.get("limit", 10)
    object = data.get("name")
    username = get_subject(request, config_)
    versions = ObjectVersions.query.filter(db.and_(ObjectVersions.owner == username, ObjectVersions.object == object)).offset(offset=offset).limit(limit).all()

    result = []

    for _ in versions:
        result.append({
            "name": _.object,
            "date_uploaded": _.date_uploaded,
            "owner": _.owner,
            "version": _.version,
            "hash": _.hash
        })
    
    return jsonify({
        "success": True,
        "result": result
    })

@mod_upload.route("/get_stl/", methods=["GET"])
def get_stl():
    if not is_valid_session(request, config_):
        return Response(
            bytes([]),
            mimetype="application/octet-stream",
            headers={
                "Content-Type": "binary"
            })
        
    object = request.args.get("object")
    version = request.args.get("version")

    username = get_subject(request, config_)
    object = ObjectVersions.query.filter(db.and_(ObjectVersions.owner == username, ObjectVersions.object == object, ObjectVersions.version == version)).first()

    if not object:
        return Response(
            bytes([]),
            mimetype="application/octet-stream",
            headers={
                "Content-Type": "binary"
            })

    file_name = hash_string(object.object + str(object.version))

    with open(f"{config_["FILE_STORAGE"]}{file_name}.stl", "rb") as f:
        data = f.read()

    print("READ BYTES:", len(data))
    print("TYPE:", type(data))  # MUST be bytes
    
    return Response(
        data,
        mimetype="application/octet-stream",
        headers={
            "Content-Type": "binary"
        }
    )

@mod_upload.route("/get_stl_info/", methods=["POST"])
def get_stl_info():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })

    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    object = data.get("name")
    version = data.get("version")

    username = get_subject(request, config_)
    object = ObjectVersions.query.filter(db.and_(ObjectVersions.owner == username, ObjectVersions.object == object, ObjectVersions.version == version)).first()

    if not object:
        return jsonify({
            "success": False,
            "reason": "Версия объекта не найдена"
        })

    return jsonify({
            "success": False,
            "result": {
                "object": object.object,
                "version": object.version,
                "surface_area": object.surface_area,
                "volume": object.volume,
                "width": object.bb_y_l,
                "length": object.bb_z_l,
                "height": object.bb_x_l,
                "is_water_tight": object.is_water_tight
            }
        })   

@mod_upload.route("/update_object_description/", methods=["POST"])
def update_object_description():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = get_subject(request, config_)
    object = Objects.query.filter_by(Objects.name == data.get("name"), Objects.owner == username).first()
    if not object:
        return jsonify({
            "success": False,
            "reason": "Object does not exist"
        })
    
    object.description = data.get("description")
    
    db.session.commit()
    
    return jsonify({
        "success": True
    })

@mod_upload.route("/delete_object_description/", methods=["POST"])
def delete_object_description():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = get_subject(request, config_)
    object = Objects.query.filter_by(Objects.name == data.get("name"), Objects.owner == username).first()
    if not object:
        return jsonify({
            "success": False,
            "reason": "Object was not found"
        })
    
    db.session.delete(object)
    
    return jsonify({
        "success": True
    })

@mod_upload.route("/upload_file/", methods=["POST"])
def upload_file():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    
    if not request.files["model"]:
        return jsonify({
            "success": False,
            "reason": "Файл не найден"
        })
    
    object = request.form.get("name")
    username = get_subject(request, config_)
    object = Objects.query.filter(db.and_(Objects.object == object, Objects.owner == username)).first()

    if not object:
        return jsonify({
            "success": False,
            "reason": "Объект не существует"
        })
    
    object_version = ObjectVersions.query.filter(db.and_(ObjectVersions.object == object.object, ObjectVersions.owner == username)).order_by(ObjectVersions.version.desc()).first()
    if not object_version:
        version = 1
    else:
        version = object_version.version + 1
    
    file_name = hash_string(object.object + str(version))
    file = request.files["model"]
    file.save(f"{config_["FILE_STORAGE"]}{file_name}.stl")
    
    object_version = ObjectVersions()
    object_version.hash = file_name
    object_version.version = version
    object_version.owner = username
    object_version.date_uploaded = datetime.now(tz=timezone.utc)
    object_version.object = object.object

    stltasks.send_task(f"{config_["FILE_STORAGE"]}{file_name}.stl", object.object, version, username)

    db.session.add(object_version)
    db.session.commit()

    return jsonify({
        "success": True
    })