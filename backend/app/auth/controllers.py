from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
import os
from binascii import hexlify
import app
from app import db
from app import config_
from models.models import Users
from models.models import Cities
from models.models import Countries
from models.models import ConfirmationTokens
from datetime import datetime
import secrets
import re
from utils.utils import check_password, encode_jwt, is_valid_auth_token, get_auth_token, decode_jwt, hash_password

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route("/register/", methods=["POST"])
def register():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = data.get("username", None)
    email = data.get("email", None)
    phone = data.get("phone", None)
    first_name = data.get("first_name", None)
    last_name = data.get("last_name", None)
    street_address = data.get("street_address", None)
    postal_code = data.get("postal_code", None)
    city_code = data.get("city_code", None)
    country_code = data.get("country_code", None)
    password = data.get("password", None)
    if not re.match(r"[a-zA-Z\._0-9]{1,20}@[A-Za-z]{1,10}\.[a-zA-Z]{1,8}", email):
        return jsonify({
            "success": False,
            "reason": "Invalid email address"
        })
    if not re.match(r"\+[0-9]{10,20}", phone):
        return jsonify({
            "success": False,
            "reason": "Invalid phone number"
        })
    if not re.match(r"[0-9]{4,10}", postal_code):
        return jsonify({
            "success": False,
            "reason": "Invalid postal code"
        })
    salt = hexlify(os.urandom(32))
    user = Users.query.filter_by(username=data.get("username", None)).first()
    if not user:
        return jsonify({
            "success": False,
            "reason": "User already exists"
        })
    country = Countries.query.filter_by(country_code=country_code).first()
    if not country:
        return jsonify({
            "success": False,
            "reason": "Invalid city"
        })
    city = Cities.query.filter_by(city_code=city_code, country_code=country_code).first()
    if not city:
        return jsonify({
            "success": False,
            "reason": "Invalid city"
        })
    user = Users()
    user.username = username
    user.password = hash_password(password, salt)
    user.salt = salt
    user.phone = phone
    user.first_name = first_name
    user.last_name = last_name
    user.street_address = street_address
    user.postal_code = postal_code
    user.city_code = city_code
    user.country_code = country_code
    user.confirmed = False
    db.session.add(user)

    confirmation = ConfirmationTokens()
    confirmation.token = hexlify(os.urandom(128))
    confirmation.username = username
    db.session.add(confirmation)

    db.session.commit()
    return jsonify({
            "success": True,
            "reason": "Verification email was sent to your address"
        })

@mod_auth.route("/confirm_email/", methods=["GET"])
def confirm_email():
    username = request.args.get("username", None)
    token = request.args.get("token", None)
    confirmation = ConfirmationTokens.query.filter_by(username=username, token=token).first()
    if not confirmation:
        return jsonify({
            "success": False,
            "reason": "Invalid confirmation token"
        })
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "success": False,
            "reason": "User does not exist"
        }) 
    user.confirmed = True
    db.session.commit()
    return jsonify({
            "success": True,
            "reason": "Email was confirmed"
        })

@mod_auth.route("/signin/", methods=["POST"])
def signin():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    salt = hexlify(os.urandom(32))
    user = Users.query.filter_by(username=data.get("username", None)).first()
        
    if user and user.confirmed and check_password(data.get("password", "").encode("UTF-8"), user.salt.encode("UTF-8"), user.password.encode("UTF-8")):
        token = encode_jwt(user.username, user.password, salt.decode("UTF-8"), config_["SERVER_NONCE"], config_["JWT_VALIDITY_IN_DAYS"], config_["TOKEN_KEY"])
        resp = make_response(jsonify({
            "success": True
        }))
        resp.set_cookie('token', token, max_age=30*24*60*60, httponly=True, secure=False, samesite='Lax')
    else:
        return jsonify({
            "success": False
        })

@mod_auth.route("/logout/", methods=["GET"])
def logout():
    resp = make_response(jsonify({
        "success": True
    }))
    resp.set_cookie('token', None, max_age=0)
    return resp

@mod_auth.route("/validate_token/", methods=["POST"])
def validate_token():
    token = get_auth_token(request)
    return jsonify({
        "valid": is_valid_auth_token(token, config_["SERVER_NONCE"], config_["TOKEN_KEY"])
    })

@mod_auth.route("/renew_token/", methods = ["POST"])
def renew_token():
    token = get_auth_token(request)
    salt = hexlify(os.urandom(32))
    payload = decode_jwt(token, config_["TOKEN_KEY"])
    if payload["server_nonce"] != config_["SERVER_NONCE"]:
        return jsonify({
            "success": False
        })
    
    if is_valid_auth_token(token, config_["SERVER_NONCE"], config_["TOKEN_KEY"]):
        token = encode_jwt(payload["subject"], salt.decode("UTF-8"), config_["SERVER_NONCE"], config_["JWT_VALIDITY_IN_DAYS"], config_["TOKEN_KEY"])
        resp = make_response(jsonify({
            "success": True
        }))
        resp.set_cookie('token', token, max_age=30*24*60*60, httponly=True, secure=False, samesite='Lax')
    return jsonify({
        "success": False
    })