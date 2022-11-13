from app import db
from app import login
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from geoalchemy2 import Geometry
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    evaluates = db.relationship("Evaluate", back_populates="user")

    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Cinema(db.Model):
    __tablename__ = "cinemas"
    id = db.Column(db.Integer, primary_key=True)
    id_supplier = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    hotline = db.Column(db.String(20))
    geom = db.Column(Geometry("POINT"))
    movie_showtimes = db.relationship(
        "Movie_showtime", back_populates="cinema", cascade="all,delete"
    )
    evaluates = db.relationship(
        "Evaluate", back_populates="cinema", cascade="all,delete"
    )
    supplier = db.relationship(
        "Supplier", back_populates="cinema", cascade="all,delete"
    )


class Movie(db.Model):
    __tablename__ = "movies"
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
    movie_showtimes = db.relationship(
        "Movie_showtime", back_populates="movie", cascade="all,delete"
    )


class Movie_showtime(db.Model):
    __tablename__ = "movie_showtimes"
    id = db.Column(db.Integer, primary_key=True)
    id_cinema = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    id_movie = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    screening_date = db.Column(db.String(50), nullable=False)
    time_start = db.Column(db.String(20))
    seats = db.Column(db.Integer)
    cinema = db.relationship(
        "Cinema", back_populates="movie_showtimes", cascade="all,delete"
    )
    movie = db.relationship(
        "Movie", back_populates="movie_showtimes", cascade="all,delete"
    )


class Evaluate(db.Model):
    __tablename__ = "evaluates"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_cinema = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    content = db.Column(db.Text)
    star_rated = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user = db.relationship("User", back_populates="evaluates", cascade="all,delete")
    cinema = db.relationship("Cinema", back_populates="evaluates", cascade="all,delete")


class Supplier(db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    img_price_ticket = db.Column(db.String, nullable=False)
    cinema = db.relationship("Cinema", back_populates="supplier", cascade="all,delete")
