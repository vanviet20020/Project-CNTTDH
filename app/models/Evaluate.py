from app import db


class Evaluate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_cinema = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    content = db.Column(db.Text)
    star_rated = db.Column(db.Integer)