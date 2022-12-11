from config import db
from werkzeug.security import generate_password_hash, check_password_hash


class Model(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.Text())
    description = db.Column(db.Text())

    def serialize(self) -> dict:
        return {"id": self.id, "name": self.name, "description": self.description}


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, email, password, role="USER"):
        self.password = generate_password_hash(password)
        self.email = email
        self.role = role

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def change_password(self, password):
        self.password = generate_password_hash(password)

    def serialize(self) -> dict:
        return {"id": self.id, "email": self.email, "role": self.role}
