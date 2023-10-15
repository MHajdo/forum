from flask import Flask
from models import db
from handlers import auth, topic

app = Flask(__name__)
db.create_all()

app.register_blueprint(auth.auth_handlers)
app.register_blueprint(topic.topic_handlers)


if __name__ == '__main__':
    app.run()
