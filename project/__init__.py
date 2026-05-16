from .db import *
from .loadenv import *
from .urls import *
from .settings import *


from user_app.app import *
project.register_blueprint(user_app)

from user_app.models import User 
with project.app_context():
    DATA_BASE.create_all()