from user_app import user_app
from user_app.views import render_main, render_login, render_register_success, render_verify
from chat_app.views import render_chat, create_chat, delete_chat

user_app.add_url_rule("/", view_func=render_main, methods=["GET", "POST"])
user_app.add_url_rule("/login", view_func=render_login, methods=["GET", "POST"])
user_app.add_url_rule("/register_success", view_func=render_register_success)
user_app.add_url_rule("/verify/<verify_code>", view_func=render_verify)

user_app.add_url_rule("/chat", view_func=render_chat)
user_app.add_url_rule("/create_chat", view_func=create_chat, methods=["POST"])
user_app.add_url_rule("/delete_chat", view_func=delete_chat, methods=["POST"])