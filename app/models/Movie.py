from app import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String, nullable=False)
    describe = db.Column(db.Text)
    director = db.Column(db.String(50), nullable=False)
    actor = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    running_time = db.Column(db.String(50), nullable=False)
    language = db.Column(db.Text)
    rated = db.Column(db.Text)
