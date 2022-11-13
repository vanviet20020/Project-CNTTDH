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
