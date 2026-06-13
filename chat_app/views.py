import flask
import flask_login
from .app import chat_app
from .models import Chat, Message
from project.db import DATA_BASE

@chat_app.route("/chat")
def render_chat():
    all_chats = Chat.query.all()
    return flask.render_template('chat.html', all_chats=all_chats)

@chat_app.route("/create_chat", methods=["POST"])
def create_chat():
    chat_name = flask.request.form.get("chat_name")
    user = flask_login.current_user
    if not user.is_authenticated:
        if chat_name:
            new_chat = Chat(name=chat_name, admin_id=1)
            DATA_BASE.session.add(new_chat)
            DATA_BASE.session.commit()
        return flask.redirect("/chat")
    
    if chat_name:
        existing_chat = Chat.query.filter_by(admin_id=user.id).first()
        if not existing_chat:
            new_chat = Chat(name=chat_name, admin_id=user.id)
            DATA_BASE.session.add(new_chat)
            DATA_BASE.session.commit()
    return flask.redirect("/chat")

@chat_app.route("/delete_chat", methods=["POST"])
def delete_chat():
    user = flask_login.current_user
    if user.is_authenticated:
        chat = Chat.query.filter_by(admin_id=user.id).first()
    else:
        chat = Chat.query.first()
    if chat:
        DATA_BASE.session.delete(chat)
        DATA_BASE.session.commit()
    return flask.redirect("/chat")

@chat_app.route("/get_messages/")
def get_messages():
    chat_id = flask.request.args.get("chat_id")
    if not chat_id:
        return flask.jsonify([])
    try:
        chat_id_int = int(chat_id)
        all_messages = Message.query.filter_by(chat_id=chat_id_int).all()
        list_messages = []
        for message in all_messages:
            list_messages.append({
                "text": message.text,
                "sender": "Пользователь"
            })
        return flask.jsonify(list_messages)
    except Exception as e:
        print(f"Помилка: {e}")
        return flask.jsonify([])
