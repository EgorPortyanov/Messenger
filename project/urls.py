from user_app import user_app
from user_app.views import render_main, render_login, render_verify, render_register_success, render_chat

user_app.add_url_rule("/", view_func=render_main, methods=["GET", "POST"])
user_app.add_url_rule("/login", view_func=render_login, methods=["GET", "POST"])
user_app.add_url_rule("/verify/<verify_code>", view_func=render_verify, methods=["GET"])
user_app.add_url_rule("/register_success", view_func=render_register_success, methods=["GET"])
user_app.add_url_rule("/chat", view_func=render_chat, methods=["GET"])