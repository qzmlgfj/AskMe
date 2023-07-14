from datetime import datetime, timedelta
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
            user = Admin.query.first()
            if user is None:
                raise RuntimeError("User not found")
            token = jwt.encode(
                {
                    "username": data["username"],
                    "ip": request.remote_addr,
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                },
                user.secret_key
            )
            return jsonify({"authenticated": True, "token": token})
        else:
            return jsonify({"authenticated": False})
    except Exception as e:
        print(e)
        return jsonify({"status": "fail"})


@auth_bp.route("register", methods=["POST"])
def register():
    try:
        if Admin.check_admin_exists():
            raise RuntimeError("Admin already exists")
        data = request.get_json()
        Admin.add(data["username"], data["password"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})


@auth_bp.route("checkadmin", methods=["GET"])
def check_admin():
    return jsonify({"status": "yes" if Admin.check_admin_exists() else "no"})
