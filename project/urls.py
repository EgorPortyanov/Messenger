from user_app import user_app
from user_app.views import render_main, render_login, render_verify

user_app.add_url_rule("/", view_func=render_main, methods=["GET", "POST"])
user_app.add_url_rule("/login", view_func=render_login, methods=["GET", "POST"])
user_app.add_url_rule("/verify/<verify_code>", view_func=render_verify, methods=["GET"])
