from app import db
from app import login
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password_input):
        self.password = generate_password_hash(password_input)

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
