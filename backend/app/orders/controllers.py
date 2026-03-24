from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response, send_file, Response
import os
from binascii import hexlify
import app
from app import db
from app import config_
from models.models import Machinery
from models.models import Colors
from models.models import Materials
from models.models import ObjectVersions
from models.models import Orders
from datetime import datetime
import secrets
import re
from datetime import tzinfo, timezone
from utils.utils import get_subject, is_valid_session, hash_string
from workers import stltasks

mod_orders = Blueprint('orders', __name__, url_prefix='/orders')

@mod_orders.route("/get_machinery/", methods=["POST"])
def get_machinery():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    username = get_subject(request, config_)

    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    object = ObjectVersions.query.filter(db.and_(ObjectVersions.object == data.get("name"), 
                                                 ObjectVersions.version == data.get("version"), 
                                                 ObjectVersions.owner == username)).first()
    if not object:
        return jsonify({
            "success": True,
            "reason": "Объект не найден"
        })
    
    printers = Machinery.query.all()
    results = []

    for p in printers:
        material = Materials.query.filter(db.and_(Materials.material == p.material, Materials.color == p.color)).first()
        color = Colors.query.filter(db.and_(Colors.color == p.color)).first()
        price = object.volume * material.price_per_cubic_cm
        
        results.append({
            "machine": p.machine,
            "dim_x": p.dimension_x,
            "dim_y": p.dimension_y,
            "dim_z": p.dimension_z,
            "overfit": (p.dimension_x < object.bb_x_l or p.dimension_y < object.bb_y_l or p.dimension_z < object.bb_z_l),
            "material": material.material,
            "material_code": material.type_code,
            "material_price_per_cm3": material.price_per_cubic_cm,
            "price": price,
            "color": color.color,
            "color_code": color.code,
            "color_desc": color.description
        })

    return jsonify({
        "success": True,
        "result": results
    })

"""
@mod_orders.route("/get_machinery/", methods=["POST"])
def get_machinery():
    if not is_valid_session(request, config_):
        return jsonify({
            "success": False,
            "auth_fail": True
        })
    username = get_subject(request, config_)

    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    object = ObjectVersions.query.filter(db.and_(ObjectVersions.object == data.get("name"), 
                                                 ObjectVersions.version == data.get("version"), 
                                                 ObjectVersions.owner == username)).first()
    if not object:
        return jsonify({
            "success": True,
            "reason": "Объект не найден"
        })
    
    order_number = hexlify(os.urandom(32)).decode("UTF-8")
    order = Orders();
    Orders.color = data.get("color")
"""