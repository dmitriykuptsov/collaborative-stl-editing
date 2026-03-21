from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
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
    
    username = get_subject(request, config_)
    objects = Objects.query.filter(db.and_(Objects.owner == username)).all()

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

    db.session.add(object_version)
    db.session.commit()

    return jsonify({
        "success": True
    })