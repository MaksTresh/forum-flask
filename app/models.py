from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    likes = db.Column(db.String())
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(30))
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.String(), index=True, default=datetime.utcnow().isoformat())
    rating = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_seen = db.Column(db.String(), default=datetime.utcnow().isoformat())

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    image = db.Column(db.String(500))
    post_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))