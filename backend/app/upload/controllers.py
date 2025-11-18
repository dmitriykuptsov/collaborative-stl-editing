from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
import os
from binascii import hexlify
import app
from app import db
from app import config_
from models.models import Users
from models.models import Objects
from datetime import datetime
import secrets
import re
from datetime import tzinfo, timezone
from utils.utils import get_subject, is_valid_session

mod_auth = Blueprint('upload', __name__, url_prefix='/upload')

@mod_auth.route("/create_object_description/", methods=["POST"])
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
    object = Objects.query.filter_by(Objects.name == data.get("name"), Objects.owner == username).first()
    if object:
        return jsonify({
            "success": False,
            "reason": "Object already exists"
        })
    
    object = Objects()
    object.name = data.get("name")
    object.description = data.get("description")
    object.owner = username
    object.creation_time = datetime.now(tz=timezone.utc)

    db.session.add(object)
    db.session.commit()
    
    return jsonify({
        "success": True
    })

@mod_auth.route("/update_object_description/", methods=["POST"])
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

@mod_auth.route("/delete_object_description/", methods=["POST"])
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

@mod_auth.route("/upload_file/", methods=["POST"])
def upload_file():
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
    
    if not request.files["model"]:
        return jsonify({
            "success": False,
            "reason": "File not found"
        })
    
    return jsonify({
        "success": True
    })