from dataclasses import dataclass
from datetime import datetime

from ..extensions import db


@dataclass
class Question(db.Model):
    id: int
    title: str
    content: str
    created_at: datetime
    private: bool

    answered: bool
    answer: str
    answered_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    private = db.Column(db.Boolean, default=False)

    answered = db.Column(db.Boolean, default=False)
    answer = db.Column(db.Text)
    answered_at = db.Column(db.DateTime)

    def __init__(self, title, content, private):
        self.title = title
        self.content = content
        self.private = private
        self.created_at = datetime.utcnow().replace(microsecond=0)

    @classmethod
    def add(cls, title, content, private):
        db.session.add(cls(title, content, private))
        db.session.commit()

    @classmethod
    def update(cls, id, title, content, private, answer):
        question = cls.query.get(id)
        question.title = title
        question.content = content
        question.private = private
        question.answer = answer
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
    def get_answered(cls):
        return cls.query.filter_by(answered=True).order_by(cls.created_at.desc()).all()

    @classmethod
    def answer_question(cls, id, answer):
        question = cls.query.get(id)
        question.answered = True
        question.answer = answer
        question.answered_at = datetime.utcnow().replace(microsecond=0)
        db.session.commit()
