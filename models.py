from sqla_wrapper import SQLAlchemy
from datetime import datetime

db = SQLAlchemy('sqlite:///my_db.sqlite')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    session_token = db.Column(db.String)


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created_at = db.Column(db.String)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)


    @classmethod
    def create(cls, title, text, author):
        topic = cls(title=title, text=text, author=author)
        db.add(topic)
        db.commit()

        return topic
