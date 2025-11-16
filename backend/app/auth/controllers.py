from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
import os
from binascii import hexlify
import app
from app import db
from app import config_
from models.models import Users
import secrets
import re
from utils.utils import check_password, encode_jwt, is_valid_auth_token, get_auth_token, decode_jwt

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route("/signin/", methods=["POST"])
def signin():
    if request.method == "POST":
        data = request.get_json(force=True)
        if not data:
            return jsonify({
                "success": False
            })
        salt = hexlify(os.urandom(32))
        user = Users.query.filter_by(username=data.get("username", None)).first()
        
        if user and check_password(data.get("password", "").encode("UTF-8"), user.salt.encode("UTF-8"), user.password.encode("UTF-8")):
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