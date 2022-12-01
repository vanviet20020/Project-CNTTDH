import json
from app import app
from app.models import *
from sqlalchemy import or_
from sqlalchemy import func
from flask import request, render_template, redirect, flash, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies, title="Trang chủ")


@app.route("/admin")
def admin():
    return render_template("user.html", title="Admin")


@app.route("/detail/<int:movie_id>")
def detail(movie_id):
    movie = Movie.query.get(movie_id)
    return render_template("detail.html", movie=movie, title="detail")


@app.route("/admin/movie")
def movie():
    return render_template("movies.html", title="Movies")


@app.route("/login")
def Login():
    return render_template("login.html", title="Movies")


@app.route("/signUp")
def signup():
    return render_template("signUp.html", title="Sign up")


@app.route("/admin/user/add")
def addUser():
    return render_template("addUser.html", title="Add User")


@app.route('/admin/movie/add')
def addMovie_s1():
    return render_template("addMovie.html", title="Add Movie")


@app.route("/addmovie", methods=["POST"])
def addmovie_s2():
    """add new movie"""

    # Get form information.
    name = request.form.get("name")
    img = request.form.get("img")
    describe = request.form.get("describe")
    director = request.form.get("director")
    actor = request.form.get("actor")
    genre = request.form.get("genre")
    running_time = request.form.get("running_time")
    release_date = request.form.get("release_date")
    language = request.form.get("language")
    rated = request.form.get("rated")
    movie = Movie(name=name, img=img, describe=describe,
                  director=director, actor=actor,
                  genre=genre, running_time=running_time,
                  release_date=release_date, language=language, rated=rated)
    db.session.add(movie)
    db.session.commit()
    return render_template("index.html")
