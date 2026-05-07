import flask, werkzeug.security, flask_login
from .models import DATA_BASE, User

def render_main():
    return flask.render_template('main.html')

def render_reg():
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        confirm_password = flask.request.form.get("confirm_password")
        if password == confirm_password:
            password_hash = werkzeug.security.generate_password_hash(password)
            user = User(username=username, email=email, password=password_hash)
            DATA_BASE.session.add(user)
            DATA_BASE.session.commit()
            return flask.redirect("/login")
    
    return flask.render_template('main.html')

def render_login():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user !=None:
            if werkzeug.security.check_password_hash(user.password, password):
                flask_login.login_user(user)
                return flask.redirect("/")
    return flask.render_template('login.html')
