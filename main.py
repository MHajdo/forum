from flask import Flask, render_template, request
from sqla_wrapper import SQLAlchemy
from datetime import datetime
from essential_generators import DocumentGenerator
from random import randint

db = SQLAlchemy('sqlite:///my_db.sqlite')

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password_hash = db.Column(db.String)
    session_token = db.Column(db.String)

class Topics(db.Model):
    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.String)
    user_id = db.Column(db.Integer)

class Messages(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created_at = db.Column(db.String)
    user_id = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)

db.create_all()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/topics')
def topics():
    generator = DocumentGenerator()
    title = generator.sentence()
    desc = generator.sentence()
    topic = Topics(title=title, description=desc, created_at=datetime.now(), user_id=1)
    db.add(topic)
    db.commit()

    return 'works'


@app.route('/posts', methods=['GET', 'POST'])
def messages():
    generator = DocumentGenerator()
    for i in range(50):
        body = generator.gen_sentence(30, 300)
        topic_id = randint(1, 5)
        user_id = randint(1, 10)
        message = Messages(body=body, created_at=datetime.now(), user_id=user_id, topic_id=topic_id)
        db.add(message)
        db.commit()

    return 'posti delajo'


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        all_users = db.query(User).all()

        return render_template('users.html', users=all_users)
    else:
        return 'post handler'


if __name__ == '__main__':
    app.run()