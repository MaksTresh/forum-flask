import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(r'C:\Users\mmaks\OneDrive\Рабочий стол\flood1lka\app', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    