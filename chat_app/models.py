from project.db import DATA_BASE

class Chat(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    name = DATA_BASE.Column(DATA_BASE.String(100), nullable=False)
    admin_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)

    @property
    def members(self):
        return ChatMember.query.filter_by(chat_id=self.id).all()


class Message(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    text = DATA_BASE.Column(DATA_BASE.String(500), nullable=False)
    sender_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    chat_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)


class ChatMember(DATA_BASE.Model):
    __tablename__ = 'chat_members'
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    user_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    chat_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)