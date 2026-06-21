from .settings import project, socketio
from .db import DATA_BASE, MIGRATE
from .login_manager import login_manager

from user_app.app import user_app
from chat_app.app import chat_app

from chat_app import socket

project.register_blueprint(user_app)
project.register_blueprint(chat_app, url_prefix="/")

from user_app import models
from chat_app import models