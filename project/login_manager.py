from .settings import project
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(project)
login_manager.login_view = "user_app.login"

@login_manager.user_loader
def load_user(user_id):
    from user_app.models import User
    return User.query.get(int(user_id))