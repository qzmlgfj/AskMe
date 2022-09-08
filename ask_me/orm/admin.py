from ..extensions import db

class Admin(db.Model):
    id: int
    username: str
    password: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    
