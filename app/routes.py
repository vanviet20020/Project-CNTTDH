import json
from app import app
from app.models import *
from sqlalchemy import or_
from sqlalchemy import func
from flask import request, render_template, redirect, flash, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
def index():
    return render_template("index.html", title="Trang chủ")


@app.route("/admin")
def admin():
    return render_template("user.html", title="Admin")


@app.route("/detail")
def detail():
    return render_template("detail.html", title="detail")


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
