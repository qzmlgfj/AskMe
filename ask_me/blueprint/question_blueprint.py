from flask import Blueprint, jsonify, request

from ..orm.question import Question
from ..wrapper import token_required


question_bp = Blueprint("/api/question", __name__, url_prefix="/api/question")

# 查看所有问题，参数为all
@question_bp.route("all", methods=["GET"])
def return_all_questions():
    return jsonify(Question.get_all())


# 查看所有问题，参数为unanswered
@question_bp.route("unanswered", methods=["GET"])
def return_unanswered_questions():
    return jsonify(Question.get_unanswered())


# 提交问题
@question_bp.route("add", methods=["POST"])
def add_question():
    try:
        data = request.get_json()
        Question.add(data["title"], data["content"], data["private"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error"})


# 回答问题
@question_bp.route("answer", methods=["POST"])
@token_required
def answer_question():
    try:
        data = request.get_json()
        Question.answer_question(data["id"], data["answer"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})


# 删除问题
@question_bp.route("delete", methods=["POST"])
@token_required
def delete_question():
    try:
        data = request.get_json()
        Question.delete(data["id"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})
