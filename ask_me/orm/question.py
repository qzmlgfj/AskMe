from dataclasses import dataclass
from datetime import datetime

from ..extensions import db


@dataclass
class Question(db.Model):
    id: int
    title: str
    question: str
    created_at: datetime

    answered: bool
    answer: str
    answered_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    question = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    answered = db.Column(db.Boolean, default=False)
    answer = db.Column(db.Text)
    answered_at = db.Column(db.DateTime)

    def __init__(self, title, question):
        self.title = title
        self.question = question
        self.created_at = datetime.utcnow().replace(microsecond=0)

    @classmethod
    def add(cls, title, question):
        db.session.add(cls(title, question))
        db.session.commit()

    @classmethod
    def update(cls, id, title, question, answer):
        question = cls.query.get(id)
        question.title = title
        question.question = question
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
    def get_unanswered(cls):
        return cls.query.filter_by(answered=False).order_by(cls.created_at.desc())

    @classmethod
    def answer_question(cls, id, answer):
        question = cls.query.get(id)
        question.answered = True
        question.answer = answer
        question.answered_at = datetime.utcnow().replace(microsecond=0)
        db.session.commit()
