from datetime import datetime
from flask import Blueprint, jsonify, request, current_app
import jwt

from ..orm.admin import Admin

auth_bp = Blueprint("/api/auth", __name__, url_prefix="/api/auth")


@auth_bp.route("loginview")
def login_view():
    return jsonify({"info": "Please Login"})


@auth_bp.route("login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if Admin.check(data["username"], data["password"]):
            token = jwt.encode(
                {
                    "iat": datetime.utcnow(),
                },
                current_app.config["SECRET_KEY"],
            )
            return jsonify({"status": "ok", "token": token})
        else:
            return jsonify({"status": "fail"})
    except Exception as e:
        print(e)
        return jsonify({"status": "fail"})


@auth_bp.route("register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        Admin.add(data["username"], data["password"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})


# @auth_bp.route("currentuser", methods=["GET"])
# def current_user_info():
#     if current_user.is_authenticated:
#         return jsonify({"username": current_user.username})
#     else:
#         return jsonify({"username": "None"})


@auth_bp.route("checkadmin", methods=["GET"])
def check_admin():
    return jsonify({"status": "yes" if Admin.check_admin_exists() else "no"})


# TODO Register时验证是否已存在Admin

# TODO Token令牌加入IP字段，防止Token被盗用
