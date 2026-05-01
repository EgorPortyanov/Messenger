from user_app import user_app
from user_app.views import render_main, render_login

user_app.add_url_rule("/", view_func=render_main)

user_app.add_url_rule("/login", view_func=render_login, methods=["GET", "POST"])