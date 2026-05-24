# import flask, werkzeug.security, flask_login
# from .models import DATA_BASE, User
# from project.login_manager import serializer

# def render_main():
#     return flask.render_template('main.html')

# def render_reg():
#     if flask.request.method == "POST":
#         username = flask.request.form.get("username")
#         email = flask.request.form.get("email")
#         password = flask.request.form.get("password")
#         confirm_password = flask.request.form.get("confirm_password")
#         if password == confirm_password:
#             password_hash = werkzeug.security.generate_password_hash(password)
#             user = User(
#                 username=username, 
#                 email=email, 
#                 password=password_hash,
#                 is_verified = False,
#                 verify_code = serializer.dumps(email, salt="email-confirm")
#             )
#             DATA_BASE.session.add(user)
#             DATA_BASE.session.commit()
    
#     return flask.render_template('reg.html')

# def render_login():
#     if flask.request.method == "POST":
#         email = flask.request.form.get("email")
#         password = flask.request.form.get("password")
#         user = User.query.filter_by(email=email).first()
#         if user !=None:
#             if werkzeug.security.check_password_hash(user.password, password):
#                 flask_login.login_user(user)
#                 return flask.redirect("/")
#     return flask.render_template('login.html')


# def render_verify(verify_code):
#     try:
#         email = serializer.loads(verify_code, salt="email-confirm", max_age = 600)
#     except:
#         return "Код не действителен"
#     user = User.query.filter_by(email=email).first()
#     if user and user.is_verified == False:
#         user.is_verified = True
#         user.verify_code = None
#         DATA_BASE.session.commit()
#     else:
#         return "Почты не существует"
    
#     return flask.redirect("/")


import flask, werkzeug.security, flask_login
from .models import DATA_BASE, User
from project.login_manager import serializer
from .mail import send_verify_code

def render_main():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        
        password_hash = werkzeug.security.generate_password_hash(password)
        token = serializer.dumps(email, salt="email-confirm")
        
        user = User(
            email=email, 
            password=password_hash,
            is_verified=False,
            verify_code=token
        )
        DATA_BASE.session.add(user)
        DATA_BASE.session.commit()
        
        send_verify_code(verify_code=token, email_receiver=email)
        
        return flask.redirect("/register_success")
            
    return flask.render_template('main.html')



def render_login():
    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if werkzeug.security.check_password_hash(user.password, password):
                flask_login.login_user(user)
                return flask.redirect("/")
    return flask.render_template('login.html')

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

def render_register_success():
    return flask.render_template('register_success.html')

def render_chat():
    return flask.render_template('chat.html')