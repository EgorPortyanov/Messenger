import flask
import flask_socketio
import flask_login
from project.settings import socketio
from .models import Chat, Message
from project.db import DATA_BASE
from user_app.models import User


@socketio.on("connect")
def handle_connect():
    print(f"Клієнт підключився: {flask.request.sid}")


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Клієнт відключився: {flask.request.sid}")


@socketio.on("connect_chat")
def handle_connect_chat(chat_id):
    if chat_id is None:
        print("Отримано пустий chat_id")
        return
    
    try:
        chat_id = int(chat_id)
    except:
        print(f"Неправильний chat_id: {chat_id}")
        return
    
    chat = Chat.query.get(chat_id)
    if chat:
        old_chat = flask.session.get("current_chat")
        if old_chat:
            flask_socketio.leave_room(old_chat)
            print(f"Вийшов з кімнати {old_chat}")
        
        room_name = f"chat_{chat_id}"
        flask_socketio.join_room(room_name)
        flask.session["current_chat"] = room_name
        print(f"Підключено до кімнати {room_name}")


@socketio.on("send")
def handle_send_message(data):
    if not isinstance(data, dict):
        return
    text = data.get("text")
    chat_id = data.get("chat_id")
    
    if not chat_id or not text:
        return
        
    chat_id = int(chat_id)
    room_name = f"chat_{chat_id}"
    user = flask_login.current_user
    
    if user.is_authenticated:
        message = Message(text=text, sender_id=user.id, chat_id=chat_id)
    else:
        message = Message(text=text, sender_id=1, chat_id=chat_id)
        
    DATA_BASE.session.add(message)
    DATA_BASE.session.commit()
    
    socketio.emit("receive_message", {
        "text": text,
        "sender": "Пользователь", 
        "message_id": message.id
    }, to=room_name)
