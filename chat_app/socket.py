import flask
import flask_socketio
import flask_login
from project.settings import socketio
from .models import Chat, Message
from project.db import DATA_BASE
from user_app.models import User

online_users = {}


@socketio.on("connect")
def handle_connect():
    print(f"Клієнт підключився: {flask.request.sid}")
    if not flask_login.current_user.is_authenticated:
        print("Неавторизований користувач, надсилаємо редирект на реєстрацію")
        socketio.emit("force_redirect", {"url": "/register"}, to=flask.request.sid)
        return

    user_id = flask_login.current_user.id
    socket_id = flask.request.sid

    flask_socketio.join_room("online")

    if user_id not in online_users:
        online_users[user_id] = set()
    online_users[user_id].add(socket_id)

    print(f"Користувач {user_id} увійшов онлайн. Всього онлайн: {len(online_users)}")

    socketio.emit("user_status", {
        "user_id": user_id,
        "status": "online"
    }, to="online")

    last_chat = flask.session.get("last_chat_id")
    if last_chat:
        socketio.emit("auto_join_chat", {"chat_id": last_chat}, to=flask.request.sid)
        print(f"Надіслано авто-підключення до чату {last_chat}")


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Клієнт відключився: {flask.request.sid}")

    if flask_login.current_user.is_authenticated:
        user_id = flask_login.current_user.id
        socket_id = flask.request.sid

        if user_id in online_users:
            online_users[user_id].discard(socket_id)
            if not online_users[user_id]:
                online_users.pop(user_id)
                print(f"Користувач {user_id} вийшов. Всього онлайн: {len(online_users)}")
                socketio.emit("user_status", {
                    "user_id": user_id,
                    "status": "offline"
                }, to="online")


@socketio.on("connect_chat")
def handle_connect_chat(chat_id):
    if not flask_login.current_user.is_authenticated:
        print("Спроба підключитися до чату без авторизації")
        socketio.emit("force_redirect", {"url": "/register"}, to=flask.request.sid)
        return

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
        flask.session.modified = True

        flask.session["last_chat_id"] = chat_id
        flask.session.modified = True

        from .models import ChatMember
        existing = ChatMember.query.filter_by(
            user_id=flask_login.current_user.id,
            chat_id=chat_id
        ).first()
        if not existing:
            new_member = ChatMember(
                user_id=flask_login.current_user.id,
                chat_id=chat_id
            )
            DATA_BASE.session.add(new_member)
            DATA_BASE.session.commit()
            print(f"Користувача {flask_login.current_user.id} додано до чату {chat_id}")

        draft = flask.session.get(f"draft_{chat_id}")
        if draft:
            socketio.emit("restore_draft", {"draft": draft}, to=flask.request.sid)
            print(f"Відновлено чернетку для чату {chat_id}: {draft[:30]}...")


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
        sender_name = f"{user.name} {user.surname}".strip() or f"User {user.id}"
    else:
        message = Message(text=text, sender_id=1, chat_id=chat_id)
        sender_name = "Користувач"
        
    DATA_BASE.session.add(message)
    DATA_BASE.session.commit()

    socketio.emit("receive_message", {
        "text": text,
        "sender": sender_name,
        "message_id": message.id,
        "chat_id": chat_id
    }, to=room_name)

    socketio.emit("global_new_message", {
        "chat_id": chat_id,
        "text": text
    }, to="online")



@socketio.on("save_draft")
def handle_save_draft(data):
    if not flask_login.current_user.is_authenticated:
        socketio.emit("force_redirect", {"url": "/register"}, to=flask.request.sid)
        return

    chat_id = data.get("chat_id")
    draft_text = data.get("draft_text")
    if chat_id and draft_text is not None:
        flask.session[f"draft_{chat_id}"] = draft_text
        flask.session.modified = True
        print(f"Чернетку для чату {chat_id} збережено")
    else:
        print("Немає даних для збереження чернетки")


@socketio.on("set_theme")
def handle_set_theme(data):
    if not flask_login.current_user.is_authenticated:
        socketio.emit("force_redirect", {"url": "/register"}, to=flask.request.sid)
        return

    theme = data.get("theme")
    if theme in ["light", "dark"]:
        flask.session["user_theme"] = theme
        flask.session.modified = True
        print(f"Тему для користувача змінено на {theme}")
        socketio.emit("theme_confirmed", {"theme": theme}, to=flask.request.sid)
    else:
        print(f"Невідома тема: {theme}")


@socketio.on("get_theme")
def handle_get_theme():
    theme = flask.session.get("user_theme", "light")
    socketio.emit("theme_loaded", {"theme": theme}, to=flask.request.sid)


def get_online_users():
    return list(online_users.keys())