from user_app.models import User
from .settings import *
import flask_login
from itsdangerous import URLSafeTimedSerializer

project.secret_key = "key"
serializer = URLSafeTimedSerializer(project.secret_key)
login_manager = flask_login.LoginManager(project)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)