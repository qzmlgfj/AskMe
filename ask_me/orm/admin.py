from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from ..extensions import db


class Admin(db.Model):
    id: int
    username: str
    password_hash: str  # 密码Hash值
    secret_key: str  # JWT密钥

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    secret_key = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.secret_key = str(uuid.uuid4())

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
        admin.password_hash = generate_password_hash(password)
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
        return check_password_hash(admin.password_hash, password)

    @classmethod
    def check_admin_exists(cls):
        return cls.query.first() is not None
