from ..extensions import db

class Admin(db.Model):
    id: int
    username: str
    password: str # 密码Hash值

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def add(cls, username, password):
        db.session.add(cls(username, password))
        db.session.commit()

    @classmethod
    def update(cls, id, username, password):
        admin = cls.query.get(id)
        admin.username = username
        admin.password = password
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
        return admin.password == password

