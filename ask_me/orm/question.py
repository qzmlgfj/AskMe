import uuid
from datetime import datetime

from ..extensions import db

# ai_flags 位编码：bit0(=1) 表示提问由 AI 发起，bit1(=2) 表示回答由 AI 撰写
# 未回答时 bit1 必须为 0（是否已回答由 answered 字段区分）
AI_QUESTION_FLAG = 1
AI_ANSWER_FLAG = 2


class Question(db.Model):
    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    private = db.Column(db.Boolean, default=False)

    answered = db.Column(db.Boolean, default=False)
    answer = db.Column(db.Text)
    answered_at = db.Column(db.DateTime)

    # AI 参与标记，位编码含义见本文件顶部常量注释
    ai_flags = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, title, content, private, ai_question=False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.private = private
        self.ai_flags = AI_QUESTION_FLAG if ai_question else 0
        # datetime.UTC于Python3.11引入，3.10及以下版本仍使用datetime.utcnow()
        self.created_at = datetime.utcnow().replace(microsecond=0)

    @property
    def is_ai_question(self):
        """提问是否由 AI 发起"""
        return bool(self.ai_flags & AI_QUESTION_FLAG)

    @is_ai_question.setter
    def is_ai_question(self, value):
        if value:
            self.ai_flags |= AI_QUESTION_FLAG
        else:
            self.ai_flags &= ~AI_QUESTION_FLAG

    @property
    def is_ai_answer(self):
        """回答是否由 AI 撰写"""
        return bool(self.ai_flags & AI_ANSWER_FLAG)

    @is_ai_answer.setter
    def is_ai_answer(self, value):
        if value:
            self.ai_flags |= AI_ANSWER_FLAG
        else:
            self.ai_flags &= ~AI_ANSWER_FLAG

    def to_dict(self):
        """API 输出结构：AI 标注以两个独立布尔暴露，位编码仅存在于存储层"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "private": self.private,
            "answered": self.answered,
            "answer": self.answer,
            "answered_at": self.answered_at.isoformat() if self.answered_at else None,
            "ai_question": self.is_ai_question,
            "ai_answer": self.is_ai_answer,
        }

    @classmethod
    def add(cls, title, content, private, ai_question=False):
        question = cls(title, content, private, ai_question=ai_question)
        db.session.add(question)
        db.session.commit()
        return question.id

    @classmethod
    def update(cls, id, title, content, private, answer, ai_question=False, ai_answer=False):
        question = cls.query.get(id)
        question.title = title
        question.content = content
        question.private = private
        question.answer = answer
        question.answered = answer != ""
        question.is_ai_question = ai_question
        # 回答被清空时同步清除 AI 回答标记
        question.is_ai_answer = answer != "" and ai_answer
        db.session.commit()

    @classmethod
    def delete(cls, id):
        question = cls.query.get(id)
        db.session.delete(question)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_unanswered(cls):
        return cls.query.filter_by(answered=False).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_unanswered_num(cls):
        return cls.query.filter_by(answered=False).count()

    @classmethod
    def unprivate_and_answered(cls):
        return cls.query.filter_by(answered=True, private=False).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_answered(cls):
        return cls.query.filter_by(answered=True).order_by(cls.created_at.desc()).all()

    @classmethod
    def answer_question(cls, id, answer, ai_answer=False):
        question = cls.query.get(id)
        question.answered = True
        question.answer = answer
        question.is_ai_answer = ai_answer
        # datetime.UTC于Python3.11引入，3.10及以下版本仍使用datetime.utcnow()
        question.answered_at = datetime.utcnow().replace(microsecond=0)
        db.session.commit()
