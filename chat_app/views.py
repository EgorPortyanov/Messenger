import flask
import flask_login
from .app import chat_app
from .models import Chat, Message, ChatMember
from project.db import DATA_BASE
from user_app.models import User
from .socket import get_online_users
from datetime import datetime


@chat_app.route("/chat")
def render_chat():
    user = flask_login.current_user
    
    if not user.is_authenticated:
        return flask.redirect("/login")
    
    my_chat = Chat.query.filter_by(admin_id=user.id).first()
    other_chats = Chat.query.filter(Chat.admin_id != user.id, Chat.admin_id != 0).all()
        
    return flask.render_template('chat.html', my_chat=my_chat, other_chats=other_chats)




@chat_app.route("/create_chat", methods=["POST"])
def create_chat():
    chat_name = flask.request.form.get("chat_name")
    user = flask_login.current_user
    
    if not user.is_authenticated:
        return flask.redirect("/login")
    
    if chat_name:
        existing_chat = Chat.query.filter_by(name=chat_name, admin_id=user.id).first()
        if not existing_chat:
            new_chat = Chat(name=chat_name, admin_id=user.id)
            DATA_BASE.session.add(new_chat)
            DATA_BASE.session.commit()
            
            from .models import ChatMember
            new_member = ChatMember(user_id=user.id, chat_id=new_chat.id)
            DATA_BASE.session.add(new_member)
            DATA_BASE.session.commit()
            
    return flask.redirect("/chat")


@chat_app.route("/delete_chat", methods=["POST"])
def delete_chat():
    user = flask_login.current_user
    if user.is_authenticated:
        chat = Chat.query.filter_by(admin_id=user.id).order_by(Chat.id.desc()).first()
        if chat:
            ChatMember.query.filter_by(chat_id=chat.id).delete()
            Message.query.filter_by(chat_id=chat.id).delete()
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
            sender = User.query.get(message.sender_id)
            if sender:
                if sender.name and sender.surname:
                    sender_name = f"{sender.name} {sender.surname}"
                elif sender.name:
                    sender_name = sender.name
                else:
                    sender_name = f"User {sender.id}"
            else:
                sender_name = "Користувач"
            list_messages.append({
                "text": message.text,
                "sender": sender_name
            })
        return flask.jsonify(list_messages)
    except Exception as e:
        print(f"Помилка: {e}")
        return flask.jsonify([])

from datetime import datetime

@chat_app.route("/get_users")
def get_users():
    chat_id = flask.request.args.get("chat_id")
    user = flask_login.current_user
    online_ids = get_online_users()
    
    if not chat_id:
        if user.is_authenticated:
            return flask.jsonify([{
                "id": user.id,
                "name": user.name or f"User {user.id}",
                "first_name": user.name or "",
                "surname": user.surname or "",
                "username": user.username or "",
                "gender": user.gender or "",
                "birth_date": user.birth_date or "",
                "is_online": user.id in online_ids
            }])
        return flask.jsonify([])
    
    try:
        chat_id_int = int(chat_id)
        members = ChatMember.query.filter_by(chat_id=chat_id_int).all()
        user_ids = [m.user_id for m in members]
        users = User.query.filter(User.id.in_(user_ids), User.is_verified == True).all()
        
        users_list = []
        for u in users:
            if u.name and u.surname:
                display_name = f"{u.name} {u.surname}"
            elif u.name:
                display_name = u.name
            else:
                display_name = f"User {u.id}"
            
            users_list.append({
                "id": u.id,
                "name": display_name,
                "first_name": u.name or "",
                "surname": u.surname or "",
                "username": u.username or "",
                "is_online": u.id in online_ids
            })
        return flask.jsonify(users_list)
    except Exception as e:
        print(f"Помилка: {e}")
        return flask.jsonify([])

@chat_app.route("/get_user_profile/<int:user_id>")
def get_user_profile(user_id):
    u = User.query.get_or_404(user_id)
    online_ids = get_online_users()
    display_name = f"{u.name} {u.surname}".strip() or f"User {u.id}"
    age_str = "Не вказано"
    formatted_date = "Не вказано"
    if u.birth_date:
        try:
            birth_dt = datetime.strptime(u.birth_date, "%Y-%m-%d")
            months = ["січ", "лют", "бер", "квіт", "трав", "черв", "лип", "серп", "вер", "жовт", "лист", "груд"]
            formatted_date = f"{birth_dt.day} {months[birth_dt.month - 1]}. {birth_dt.year}"
            
            today = datetime.now()
            age = today.year - birth_dt.year - ((today.month, today.day) < (birth_dt.month, birth_dt.day))
            
            if age % 10 == 1 and age % 100 != 11:
                suffix = "рік"
            elif age % 10 in [2, 3, 4] and age % 100 not in [11, 12, 13, 14]:
                suffix = "роки"
            else:
                suffix = "років"
                
            age_str = f"{age} {suffix}"
        except Exception as e:
            print(f"Помилка парсингу дати: {e}")

    return flask.jsonify({
        "id": u.id,
        "name": display_name,
        "first_name": u.name or "",
        "surname": u.surname or "",
        "username": u.username or f"user{u.id}",
        "gender": u.gender or "Не вказано",
        "birth_date_text": f"{formatted_date} ({age_str})" if u.birth_date else "Не вказано",
        "is_online": u.id in online_ids
    })

@chat_app.route("/update_profile", methods=["POST"])
def update_profile():
    user = flask_login.current_user
    if not user.is_authenticated:
        return flask.jsonify({"error": "Не авторизований"}), 401
    
    data = flask.request.get_json()
    
    user.name = data.get("name", "")
    user.surname = data.get("surname", "")
    user.username = data.get("username", "")
    user.gender = data.get("gender", "")
    user.birth_date = data.get("birth_date", "")
    
    DATA_BASE.session.commit()
    
    return flask.jsonify({"success": True})

