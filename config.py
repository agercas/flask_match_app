import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if SECRET_KEY is None:
        raise ValueError("No SECRET_KEY set for Flask application")

    if SQLALCHEMY_DATABASE_URI is None:
        raise ValueError("No SQLALCHEMY_DATABASE_URI set for Flask application")
