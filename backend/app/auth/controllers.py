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
from datetime import datetime, timedelta
import secrets
import re
from utils.utils import check_password, encode_jwt, is_valid_auth_token, get_auth_token, decode_jwt, hash_password
from utils.email import send_account_confirmation, send_password_reset_confirmation

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

@mod_auth.route("/get_contries/", methods=["POST"])
def get_contries():
    countries = Countries.query.all()
    result = []
    for _ in countries:
        result.append({
            "code": _.country_code,
            "country": _.country
        })
    return jsonify({
            "success": True,
            "result": result
        })

@mod_auth.route("/get_cities/", methods=["POST"])
def get_cities():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    country = data.get("country", None)
    cities = Cities.query.filter_by(country_code=country).all()
    result = []
    for _ in cities:
        result.append({
            "code": _.city_code,
            "city": _.city
        })
    return jsonify({
            "success": True,
            "result": result
        })

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
            "reason": "Неверный адрес электронной почты"
        })
    if not re.match(r"\+[0-9_\-\+]{10,20}", phone):
        return jsonify({
            "success": False,
            "reason": "Неверный формат номера телефона"
        })
    if not re.match(r"[0-9]{4,10}", postal_code):
        return jsonify({
            "success": False,
            "reason": "Неверный формат почтового индекса"
        })
    salt = hexlify(os.urandom(32)).decode("UTF-8")
    if not username:
        return jsonify({
            "success": False,
            "reason": "Неверное имя пользователя"
        })
    user = Users.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "success": False,
            "reason": "Пользователь уже существует"
        })
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "success": False,
            "reason": "Пользователь уже существует"
        })
    country = Countries.query.filter_by(country_code=country_code).first()
    if not country:
        return jsonify({
            "success": False,
            "reason": "Неверный код страны"
        })
    city = Cities.query.filter_by(city_code=city_code, country_code=country_code).first()
    if not city:
        return jsonify({
            "success": False,
            "reason": "Неверный код города"
        })
    user = Users()
    user.username = username
    user.password = hash_password(password, salt)
    user.email = email
    user.salt = salt
    user.phone = phone
    user.first_name = first_name
    user.last_name = last_name
    user.street_address = street_address
    user.postal_code = postal_code
    user.city_code = city_code
    user.country_code = country_code
    user.confirmed = False
    user.enable_two_factor_auth = False
    db.session.add(user)
    db.session.commit()

    now = datetime.now()
    token_exp = now + timedelta(days=1)

    confirmation = ConfirmationTokens()
    confirmation.token = hexlify(os.urandom(32)).decode("UTF-8")
    confirmation.username = username
    confirmation.exp = int(token_exp.timestamp())

    #send_account_confirmation(username, user.email, confirmation.token)

    db.session.add(confirmation)

    db.session.commit()
    return jsonify({
            "success": True,
            "reason": "Код подтверждения был отправлен на электронную почту"
        })

@mod_auth.route("/confirm_email/", methods=["POST"])
def confirm_email():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    
    username = data.get("username", None)
    token = data.get("token", None)
    confirmation = ConfirmationTokens.query.filter_by(username=username, token=token).first()
    if not confirmation:
        return jsonify({
            "success": False,
            "reason": "Неверный код подтверждения"
        })
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "success": False,
            "reason": "Пользователь не существует"
        })
    
    if user.confirmed:
        return jsonify({
            "success": True,
            "reason": "Учетная запись подтверждена"
        })
    
    if datetime.now().timestamp() > confirmation.exp:
        return jsonify({
            "success": False,
            "reason": "Неверный код подтверждения"
        })
    
    user.confirmed = True
    db.session.commit()

    return jsonify({
            "success": True,
            "reason": "Учетная запись подтверждена"
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
        resp.set_cookie('token', token, max_age=30*24*60*60, httponly=True, secure=False, samesite='Lax', domain="localhost")
        #resp.set_cookie('token', token, max_age=30*24*60*60, httponly=True, secure=False)
        return resp
    else:
        return jsonify({
            "success": False
        })
    
@mod_auth.route("/reset_password_request/", methods=["POST"])
def reset_password_request():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = data.get("username", None)
    email = data.get("email", None)

    user = Users.query.filter_by(db.or_(username=username, email=email)).first()

    if not user:
        return jsonify({
            "success": False,
            "reason": "Пользователь не найден"
        })
    
    now = datetime.now()
    token_exp = now + timedelta(days=1)
    confirmation = ConfirmationTokens()
    confirmation.token = hexlify(os.urandom(32)).decode("UTF-8")
    confirmation.username = username
    confirmation.exp = int(token_exp.timestamp())
    send_password_reset_confirmation(username, user.email, confirmation.token)
    db.session.add(confirmation)
    db.session.commit()
    return jsonify({
            "success": True
        })

@mod_auth.route("/reset_password/", methods=["POST"])
def reset_password():
    data = request.get_json(force=True)
    if not data:
        return jsonify({
            "success": False
        })
    username = data.get("username", None)
    token = data.get("token", None)
    password = data.get("password", None)

    confirmation = ConfirmationTokens.query.filter_by(username=username, token=token).first()
    
    if not confirmation:
        return jsonify({
            "success": False,
            "reason": "Неверный код подтверждения"
        })
    
    user = Users.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({
            "success": False,
            "reason": "Пользователь не существует"
        })
    
    if not user.confirmed:
        return jsonify({
            "success": True,
            "reason": "Учетная запись не подтверждена"
        })
    
    if datetime.now().timestamp() > confirmation.exp:
        return jsonify({
            "success": False,
            "reason": "Неверный код подтверждения"
        })
    db.session.delete(confirmation)
    db.session.commit()

    salt = hexlify(os.urandom(32))
    
    user.password = hash_password(password, salt)
    user.salt = salt
    
    db.session.commit()

    return jsonify({
            "success": True,
            "reason": "Пароль был изменен"
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
        if payload["exp"] < int(datetime.now().timestamp()) - 10*60:
            token = encode_jwt(payload["subject"], salt.decode("UTF-8"), config_["SERVER_NONCE"], config_["JWT_VALIDITY_IN_DAYS"], config_["TOKEN_KEY"])
            resp = make_response(jsonify({
                "success": True
            }))
            resp.set_cookie('token', token, max_age=24*60*60, httponly=True, secure=False, samesite='Lax')
        else:
            return jsonify({
                "success": True
            })
    return jsonify({
        "success": False
    })