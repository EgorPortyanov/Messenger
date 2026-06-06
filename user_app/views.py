import flask
import werkzeug.security
import flask_login
from .models import User
from .app import user_app
from project.db import DATA_BASE
from project.login_manager import serializer


@user_app.route("/", methods=["GET", "POST"])
def render_main():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        confirm_password = flask.request.form.get("confirm_password")
        
        if password != confirm_password:
            return "Паролі не співпадають", 400
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Користувач з такою поштою вже існує", 400
        
        password_hash = werkzeug.security.generate_password_hash(password)
        user = User(email=email, password=password_hash)
        DATA_BASE.session.add(user)
        DATA_BASE.session.commit()
        
        return flask.redirect("/register_success")
    
    return flask.render_template('main.html')


@user_app.route("/login", methods=["GET", "POST"])
def render_login():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user and werkzeug.security.check_password_hash(user.password, password):
            flask_login.login_user(user)
            return flask.redirect("/chat")
    
    return flask.render_template('login.html')


@user_app.route("/register_success")
def render_register_success():
    return flask.render_template('register_success.html')


@user_app.route("/verify/<verify_code>")
def render_verify(verify_code):
    try:
        email = serializer.loads(verify_code, salt="email-confirm", max_age=600)
    except:
        return "Код не действителен или истек срок действия (10 минут)."
        
    user = User.query.filter_by(email=email).first()
    if user and user.is_verified == False:
        user.is_verified = True
        user.verify_code = None
        DATA_BASE.session.commit()
    else:
        return "Пользователь не найден или уже подтвержден."
    
    return flask.redirect("/")