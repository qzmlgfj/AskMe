from flask import Blueprint, jsonify, request

question_bp = Blueprint("/api/question", __name__, url_prefix="/api/question")

# @question_bp.route("basic_status", methods=["GET"])
# def return_basic_status():
#     return jsonify(Status.utils.get_basic_status())
