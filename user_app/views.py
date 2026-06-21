import flask
import werkzeug.security
import flask_login
from .models import User
from .app import user_app
from project.db import DATA_BASE
from itsdangerous import URLSafeTimedSerializer
from .mail import send_verify_code

serializer = None

@user_app.before_app_request
def init_serializer():
    global serializer
    if serializer is None:
        serializer = URLSafeTimedSerializer(flask.current_app.config["SECRET_KEY"])


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
        
        token = serializer.dumps(email, salt="email-confirm")
        
        password_hash = werkzeug.security.generate_password_hash(password)
        user = User(
            email=email, 
            password=password_hash, 
            verify_code=token,
            is_verified=False
        )
        DATA_BASE.session.add(user)
        DATA_BASE.session.commit()
        
        send_verify_code(token, email)
        print(f"Лист надіслано на {email}")
        
        return flask.redirect("/register_success")
    
    return flask.render_template('main.html')


@user_app.route("/login", methods=["GET", "POST"])
def render_login():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user and werkzeug.security.check_password_hash(user.password, password):
            if not user.is_verified:
                return "Будь ласка, підтвердіть свою пошту перед входом. Перевірте вашу поштову скриньку.", 400
            
            flask_login.login_user(user)
            return flask.redirect("/chat")
        else:
            return "Неправильна пошта або пароль", 400
    
    return flask.render_template('login.html')


@user_app.route("/register_success")
def render_register_success():
    return flask.render_template('register_success.html')


@user_app.route("/verify/<token>")
def render_verify(token):
    global serializer
    if serializer is None:
        serializer = URLSafeTimedSerializer(flask.current_app.config["SECRET_KEY"])
    
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=600)
    except Exception as e:
        print(f"Помилка верифікації: {e}")
        return "Код не действителен или истек срок действия (10 минут).", 400
        
    user = User.query.filter_by(email=email).first()
    if user and user.is_verified == False:
        user.is_verified = True
        user.verify_code = None
        DATA_BASE.session.commit()
        return "Пошту підтверджено! Тепер ви можете <a href='/login'>увійти</a>."
    else:
        return "Пользователь не найден или уже подтвержден.", 400
    
@user_app.route("/logout")
def render_logout():
    flask_login.logout_user()
    return flask.redirect("/login")
