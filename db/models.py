from config import db

class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.Text())

    def serialize(self) -> dict:
        return {"id": self.id, "name": self.name}