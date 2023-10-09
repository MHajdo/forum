from flask import Flask, render_template, request, make_response
from sqla_wrapper import SQLAlchemy
from datetime import datetime
from essential_generators import DocumentGenerator
from random import randint
import hashlib
import uuid

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
    user = None
    session_id = request.cookies.get('session_token')
    if session_id:
        user = db.query(User).filter_by(session_token=session_id).first()

    if user:
        message=f'logged in with user "{user.username}"'
    return render_template('index.html', msg=message)


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


@app.route('/sign-up', methods=['GET', 'POST'])
def user_sign_up():
    if request.method == 'GET':
        all_users = db.query(User).all()

        return render_template('sign-up.html', users=all_users)
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        session_token = str(uuid.uuid4())
        user = User(username=username, email=email, password_hash=hashed_password, session_token=session_token)
        db.add(user)
        db.commit()

        response = make_response('signup successful')
        response.set_cookie('session_token', session_token)
        return response


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        all_users = db.query(User).all()

        return render_template('login.html', users=all_users)
    else:
        username = request.form.get('username')
        hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        user = db.query(User).filter_by(username=username, password_hash=hashed_password).first()
        if user:
            response = make_response('login successful')
            response.set_cookie('session_token', user.session_token)
            return response
        else:
            return 'login failed'


if __name__ == '__main__':
    app.run()