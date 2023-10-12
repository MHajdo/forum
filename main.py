from flask import Flask, render_template, request, make_response, redirect, url_for, abort
from datetime import datetime
from essential_generators import DocumentGenerator
from random import randint
from models import Users, Topics, Messages, db
import hashlib
import uuid
import os
import smartninja_redis

redis = smartninja_redis.from_url(os.environ.get('REDIS_URL'))


app = Flask(__name__)
db.create_all()


def get_user(session_id=None):
    if not session_id:
        session_id = request.cookies.get('session_token')
    return db.query(Users).filter_by(session_token=session_id).first()


@app.route('/')
def index():
    user = get_user()
    return render_template('index.html', user=user)


@app.route('/topics', methods=['GET', 'POST'])
def topics():
    topic = db.query(Topics).all()
    return render_template('topics.html', topic=topic)


@app.route('/topics/<topic_id>', methods=['GET'])
def topics_topic_detail(topic_id):
    try:
        topic_id = int(topic_id)
    except ValueError:
        return abort(404)

    topic = db.query(Topics).filter_by(id=int(topic_id)).first()
    return render_template('topic.html', topic=topic)


@app.route('/topics/new-topic', methods=['GET', 'POST'])
def topics_new_topic():
    user = get_user()
    if not user:
        return redirect(url_for('login'))

    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=user.username)

    if request.method == 'GET':
        return render_template('topics-new-topic.html', csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')
        redis_csrf_uname = redis.get(name=csrf_token)
        if redis_csrf_uname and redis_csrf_uname == user.username:
            title = request.form.get('topic-title')
            text = request.form.get('topic-text')


            topic = Topics.create(title=title, text=text, author=user)
            return redirect(url_for('topics'))
        else:
            return abort(403)


#@app.route('/posts', methods=['GET', 'POST'])
#def messages():
#    generator = DocumentGenerator()
#    for i in range(50):
#        body = generator.gen_sentence(30, 300)
#        topic_id = randint(1, 5)
#        user_id = randint(1, 10)
#        message = Messages(body=body, created_at=datetime.now(), user_id=user_id, topic_id=topic_id)
#        db.add(message)
#        db.commit()
#
#    return 'posti delajo'


@app.route('/sign-up', methods=['GET', 'POST'])
def user_sign_up():
    if request.method == 'GET':
        all_users = db.query(Users).all()

        return render_template('sign-up.html', users=all_users)
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        session_token = str(uuid.uuid4())
        user = Users(username=username, email=email, password_hash=hashed_password, session_token=session_token)
        db.add(user)
        db.commit()

        response = make_response('signup successful')
        response.set_cookie('session_token', session_token)
        return response


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        all_users = db.query(Users).all()

        return render_template('login.html', users=all_users)
    else:
        username = request.form.get('username')
        hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        user = db.query(Users).filter_by(username=username, password_hash=hashed_password).first()
        if user:
            response = make_response('login successful')
            response.set_cookie('session_token', user.session_token)
            return response
        else:
            return redirect(url_for('user_sign_up'))


if __name__ == '__main__':
    app.run()