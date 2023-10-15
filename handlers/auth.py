from flask import request, render_template, make_response, redirect, url_for, Blueprint
import hashlib
import uuid
from models import Users, db

auth_handlers = Blueprint('auth_handlers', __name__)


def get_user(session_id=None):
    if not session_id:
        session_id = request.cookies.get('session_token')
    return db.query(Users).filter_by(session_token=session_id).first()


@auth_handlers.route('/sign-up', methods=['GET', 'POST'])
def user_sign_up():
    if request.method == 'GET':
        all_users = db.query(Users).all()

        return render_template('auth/sign-up.html', users=all_users)
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


@auth_handlers.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        all_users = db.query(Users).all()

        return render_template('auth/login.html', users=all_users)
    else:
        username = request.form.get('username')
        hashed_password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        user = db.query(Users).filter_by(username=username, password_hash=hashed_password).first()
        if user:
            response = make_response('login successful')
            response.set_cookie('session_token', user.session_token)
            return response
        else:
            return redirect(url_for('auth_handlers.user_sign_up'))
