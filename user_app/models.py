from project.db import DATA_BASE 
import flask_login

class User(DATA_BASE.Model, flask_login.UserMixin):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    password = DATA_BASE.Column(DATA_BASE.String)
    email = DATA_BASE.Column(DATA_BASE.String, unique=True)
    is_verified = DATA_BASE.Column(DATA_BASE.Boolean, default=False)
    verify_code = DATA_BASE.Column(DATA_BASE.String)
    
    # my_chat = DATA_BASE.relationship("Chat", back_populates="admin")
    
    # my_messages = DATA_BASE.relationship("Message", back_populates="sender")

    # chats = DATA_BASE.relationship("UserChat", back_populates="user")