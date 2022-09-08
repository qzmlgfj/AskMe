from dataclasses import dataclass
from datetime import datetime

from ..extensions import db


@dataclass
class Question(db.Model):
    id: int
    title: str
    body: str
    created_at: datetime

    answered: bool
    answer: str
    answered_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    answered = db.Column(db.Boolean, default=False)
    answer = db.Column(db.Text)
    answered_at = db.Column(db.DateTime)
