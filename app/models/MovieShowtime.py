from app import db


class Movie_showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screening_date = db.Column(db.String(50), nullable=False)
    time_start = db.Column(db.String(20))
    seats = db.Column(db.Integer)
    id_cinema = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    id_movie = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)