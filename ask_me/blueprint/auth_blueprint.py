from flask import Blueprint, jsonify, request, render_template
from flask_login import login_user, logout_user, login_required

from ..orm.admin import Admin
from flask_login import current_user

auth_bp = Blueprint("/api/auth", __name__, url_prefix="/api/auth")

@auth_bp.route("loginview")
def login_view():
    return jsonify({"info": "Please Login"})

@auth_bp.route("login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        admin = Admin.get_by_username(data["username"])
        if admin is not None and Admin.check(data["username"], data["password"]):
            login_user(admin)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "fail"})
    except Exception as e:
        return jsonify({"status": "fail"})

@auth_bp.route("currentuser", methods=["GET"])
def current_user_info():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})
    else:
        return jsonify({"username": "None"})
