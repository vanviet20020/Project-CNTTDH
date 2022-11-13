from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"


from app.models import User, Cinema, Movie, MovieShowtime, Evaluate, Supplier
from app import routes