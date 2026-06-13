# from project.db import DATA_BASE

# class Chat(DATA_BASE.Model):
#     id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
#     name = DATA_BASE.Column(DATA_BASE.String)
#     admin_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("user.id"), unique=True)
    
#     # admin = DATA_BASE.relationship("User", back_populates="my_chat")
#     # messages = DATA_BASE.relationship("Message", back_populates="chat")
#     # members = DATA_BASE.relationship("UserChat", back_populates="chat")

# class Message(DATA_BASE.Model):
#     id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
#     text = DATA_BASE.Column(DATA_BASE.String)
#     sender_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("user.id"))
    
#     # sender = DATA_BASE.relationship("User", back_populates="my_messages")

#     chat_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("chat.id"))
#     # chat = DATA_BASE.relationship("Chat", back_populates="messages")

# class UserChat(DATA_BASE.Model):
    
#     id = DATA_BASE.Column(DATA_BASE.Integer, primary_key = True)
#     user_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("user.id"), nullable = False)
#     chat_id = DATA_BASE.Column(DATA_BASE.Integer, DATA_BASE.ForeignKey("chat.id"), nullable = False)

#     # user = DATA_BASE.relationship("User", back_populates="chats")
#     # chat = DATA_BASE.relationship("Chat", back_populates="members")



from project.db import DATA_BASE

class Chat(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    name = DATA_BASE.Column(DATA_BASE.String(100), nullable=False)
    admin_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)


class Message(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    text = DATA_BASE.Column(DATA_BASE.String(500), nullable=False)
    sender_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    chat_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)