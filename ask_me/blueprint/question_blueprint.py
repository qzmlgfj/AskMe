from flask import Blueprint, jsonify, request

from ..orm.question import Question
from ..wrapper import token_required


question_bp = Blueprint("/api/question", __name__, url_prefix="/api/question")

# 查看所有问题，参数为all
@question_bp.route("all", methods=["GET"])
def return_all_questions():
    return jsonify(Question.get_all())


# 查看未回答问题，参数为unanswered
@question_bp.route("unanswered", methods=["GET"])
def return_unanswered_questions():
    return jsonify(Question.get_unanswered())


# 查看未回答问题数量
@question_bp.route("unanswered_num", methods=["GET"])
def return_unanswered_num():
    return jsonify({"num": Question.get_unanswered_num()})


# 查看已回答问题，参数为answered
@question_bp.route("answered", methods=["GET"])
def return_answered_questions():
    return jsonify(Question.get_answered())


# 查看指定id问题
@question_bp.route("<int:question_id>", methods=["GET"])
def return_question(question_id):
    return jsonify(Question.get_by_id(question_id))


# 提交问题
@question_bp.route("add", methods=["POST"])
def add_question():
    try:
        data = request.get_json()
        Question.add(data["title"], data["content"], data["private"])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})


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


# 修改问题
@question_bp.route("edit", methods=["POST"])
@token_required
def edit_question():
    try:
        data = request.get_json()
        Question.update(
            data["id"], data["title"], data["content"], data["private"], data["answer"]
        )
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail"})
