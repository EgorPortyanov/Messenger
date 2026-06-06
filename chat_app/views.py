import flask
from .app import chat_app
from .models import Chat
from project.db import DATA_BASE


@chat_app.route("/chat")
def render_chat():
    user_chat = Chat.query.first()
    return flask.render_template('chat.html', user_chat=user_chat)


@chat_app.route("/create_chat", methods=["POST"])
def create_chat():
    chat_name = flask.request.form.get("chat_name")  
    existing_chat = Chat.query.first()
    
    if chat_name and not existing_chat:
        new_chat = Chat(name=chat_name)
        DATA_BASE.session.add(new_chat)
        DATA_BASE.session.commit()
    
    return flask.redirect("/chat")


@chat_app.route("/delete_chat", methods=["POST"])
def delete_chat():
    chat = Chat.query.first()
    if chat:
        DATA_BASE.session.delete(chat)
        DATA_BASE.session.commit()
    
    return flask.redirect("/chat")