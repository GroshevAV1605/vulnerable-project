from app import db, login
import datetime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author")


    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(128))
    content = db.Column(db.String(1024))
    date = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)


    def __repr__(self):
        return '<Post {}>'.format(self.title)

