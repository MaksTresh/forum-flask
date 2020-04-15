import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.path.abspath("app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    