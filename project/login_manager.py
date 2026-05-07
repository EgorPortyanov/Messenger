from .settings import *
from user_app.models import User
import flask_login

project.secret_key = "key"
login_manager = flask_login.LoginManager()

@login_manager.user_loader
def load_user(id: int):
    return User.query.get(id)