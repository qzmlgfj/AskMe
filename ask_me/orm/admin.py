from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db, login_manager


class Admin(UserMixin, db.Model):
    id: int
    username: str
    password_hash: str  # 密码Hash值

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def get_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def add(cls, username, password):
        db.session.add(cls(username, password))
        db.session.commit()

    @classmethod
    def update(cls, id, username, password):
        admin = cls.query.get(id)
        admin.username = username
        admin.password = generate_password_hash(password)
        db.session.commit()

    @classmethod
    def delete(cls, id):
        admin = cls.query.get(id)
        db.session.delete(admin)
        db.session.commit()

    @classmethod
    def check(cls, username, password):
        admin = cls.query.filter_by(username=username).first()
        if admin is None:
            return False
        return check_password_hash(admin.password, password)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(user_id)
