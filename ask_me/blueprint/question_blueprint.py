from datetime import datetime

from flask import Blueprint, current_app, jsonify, request

from ..extensions import db
from ..orm.question import Question
from ..wrapper import token_required


question_bp = Blueprint("/api/question", __name__, url_prefix="/api/question")


def _format_import_error(item, error):
    item_id = item.get("id", "<missing-id>") if isinstance(item, dict) else "<invalid-item>"
    return {"id": item_id, "message": str(error)}

# 查看所有问题，参数为all
@question_bp.route("all", methods=["GET"])
@token_required
def return_all_questions():
    return jsonify(Question.get_all())


# 查看未回答问题，参数为unanswered
@question_bp.route("unanswered", methods=["GET"])
@token_required
def return_unanswered_questions():
    return jsonify(Question.get_unanswered())


# 查看未回答问题数量
@question_bp.route("unanswered_num", methods=["GET"])
def return_unanswered_num():
    return jsonify({"num": Question.get_unanswered_num()})


# 查看已回答问题，参数为answered
@question_bp.route("unprivate_and_answered", methods=["GET"])
def return_unprivate_and_answered_questions():
    return jsonify(Question.unprivate_and_answered())


# 查看已回答问题，参数为admin_answered，包含私密问题
@question_bp.route("admin_answered", methods=["GET"])
@token_required
def return_answered_questions():
    return jsonify(Question.get_answered())


# 查看指定id问题
@question_bp.route("/get_question/<question_id>", methods=["GET"])
def return_question(question_id):
    result = Question.get_by_id(question_id)
    return jsonify([result]) if result else jsonify([])


# 提交问题
@question_bp.route("add", methods=["POST"])
def add_question():
    try:
        data = request.get_json()
        id = Question.add(data["title"], data["content"], data["private"])
        return jsonify({"status": "ok", "id": id})
    except Exception as e:
        current_app.logger.error(f"Add question failed: {e}")
        return jsonify({"status": "fail", "message": str(e)})


# 回答问题
@question_bp.route("answer", methods=["POST"])
@token_required
def answer_question():
    try:
        data = request.get_json()
        Question.answer_question(data["id"], data["answer"])
        return jsonify({"status": "ok"})
    except Exception as e:
        current_app.logger.error(f"Answer question failed: {e}")
        return jsonify({"status": "fail", "message": str(e)})


# 删除问题
@question_bp.route("delete", methods=["POST"])
@token_required
def delete_question():
    try:
        data = request.get_json()
        Question.delete(data["id"])
        return jsonify({"status": "ok"})
    except Exception as e:
        current_app.logger.error(f"Delete question failed: {e}")
        return jsonify({"status": "fail", "message": str(e)})


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
        current_app.logger.error(f"Edit question failed: {e}")
        return jsonify({"status": "fail", "message": str(e)})


# 导出所有问题
@question_bp.route("export", methods=["GET"])
@token_required
def export_questions():
    questions = Question.get_all()
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "created_at": q.created_at.isoformat() if q.created_at else None,
            "private": q.private,
            "answered": q.answered,
            "answer": q.answer,
            "answered_at": q.answered_at.isoformat() if q.answered_at else None,
        })
    return jsonify(result)


# 导入问题
@question_bp.route("import", methods=["POST"])
@token_required
def import_questions():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"status": "fail", "message": "data must be a list"})

        imported = 0
        updated = 0
        failed = []
        for item in data:
            sp = None
            try:
                if not isinstance(item, dict):
                    raise ValueError("item must be an object")
                if not item.get("id"):
                    raise ValueError("missing required field: id")
                if "title" not in item:
                    raise ValueError("missing required field: title")
                if "content" not in item:
                    raise ValueError("missing required field: content")

                sp = db.session.begin_nested()
                question = Question.query.get(item["id"])
                created_at = datetime.fromisoformat(item["created_at"]) if item.get("created_at") else None
                answered_at = datetime.fromisoformat(item["answered_at"]) if item.get("answered_at") else None
                if question:
                    question.title = item["title"]
                    question.content = item["content"]
                    question.private = item.get("private", False)
                    question.answered = item.get("answered", False)
                    question.answer = item.get("answer")
                    question.created_at = created_at
                    question.answered_at = answered_at
                    updated += 1
                else:
                    question = Question(item["title"], item["content"], item.get("private", False))
                    question.id = item["id"]
                    question.answered = item.get("answered", False)
                    question.answer = item.get("answer")
                    question.created_at = created_at
                    question.answered_at = answered_at
                    db.session.add(question)
                    imported += 1
                sp.commit()
            except Exception as e:
                if sp is not None:
                    sp.rollback()
                current_app.logger.error(
                    f"Import question failed for item {item if isinstance(item, dict) else repr(item)}: {e}"
                )
                failed.append(_format_import_error(item, e))
        db.session.commit()
        return jsonify(
            {
                "status": "ok",
                "result": {
                    "imported": imported,
                    "updated": updated,
                    "failed": failed,
                },
            }
        )
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Import questions failed: {e}")
        return jsonify({"status": "fail", "message": str(e)})
