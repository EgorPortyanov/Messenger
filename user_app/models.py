from project.db import DATA_BASE 
import flask_login

class User(DATA_BASE.Model, flask_login.UserMixin):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    password = DATA_BASE.Column(DATA_BASE.String)
    email = DATA_BASE.Column(DATA_BASE.String, unique=True)
    is_verified = DATA_BASE.Column(DATA_BASE.Boolean, default=False)
    verify_code = DATA_BASE.Column(DATA_BASE.String)
    
    my_chat = DATA_BASE.relationship("Chat", back_populates="admin")
    
    my_messages = DATA_BASE.relationship("Message", back_populates="sender")

class Chat(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    name = DATA_BASE.Column(DATA_BASE.String)
    admin_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("user.id"), unique=True)
    
    admin = DATA_BASE.relationship("User", back_populates="my_chat")
    messages = DATA_BASE.relationship("Message", back_populates="chat")

class Message(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    text = DATA_BASE.Column(DATA_BASE.String)
    sender_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("user.id"))
    
    sender = DATA_BASE.relationship("User", back_populates="my_messages")

    chat_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("chat.id"))
    chat = DATA_BASE.relationship("Chat", back_populates="messages")
