import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "cannot-be-guess"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:nguyentoan@localhost:5432/Cimera"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print("Connect to database successfully!")
