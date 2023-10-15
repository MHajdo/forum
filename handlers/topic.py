from flask import render_template, redirect, url_for, request, abort, Blueprint
from models import db, Topics
import uuid
from redis import redis
from handlers.auth import get_user

topic_handlers = Blueprint('topic_handlers', __name__)


@topic_handlers.route('/')
def index():
    user = get_user()
    return render_template('topic/index.html', user=user)


@topic_handlers.route('/topics', methods=['GET', 'POST'])
def topics():
    topic = db.query(Topics).all()
    return render_template('topic/topics.html', topic=topic)


@topic_handlers.route('/topics/<topic_id>', methods=['GET'])
def topics_topic_detail(topic_id):
    try:
        topic_id = int(topic_id)
    except ValueError:
        return abort(404)

    topic = db.query(Topics).filter_by(id=int(topic_id)).first()
    return render_template('topic/topic.html', topic=topic)


@topic_handlers.route('/topics/new-topic', methods=['GET', 'POST'])
def topics_new_topic():
    user = get_user()
    if not user:
        return redirect(url_for('auth_handlers.login'))

    csrf_token = str(uuid.uuid4())
    redis.set(name=csrf_token, value=user.username)

    if request.method == 'GET':
        return render_template('topic/topics-new-topic.html', csrf_token=csrf_token)
    else:
        csrf_token = request.form.get('csrf_token')
        redis_csrf_uname = redis.get(name=csrf_token).decode()
        if redis_csrf_uname and redis_csrf_uname == user.username:
            title = request.form.get('topic-title')
            text = request.form.get('topic-text')

            topic = Topics.create(title=title, text=text, author=user)
            return redirect(url_for('topic_handlers.topics'))
        else:
            return abort(403)
