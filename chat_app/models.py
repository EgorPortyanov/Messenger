from project.db import DATA_BASE
from datetime import datetime

class Chat(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    name = DATA_BASE.Column(DATA_BASE.String(100), nullable=False)
    admin_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    
    @property
    def members(self):
        return ChatMember.query.filter_by(chat_id=self.id).all()

    def get_last_message(self):
        return Message.query.filter_by(chat_id=self.id).order_by(Message.timestamp.desc()).first()

    def get_unread_count(self, user_id):
        return Message.query.filter_by(chat_id=self.id, is_read=False).filter(Message.sender_id != user_id).count()


class Message(DATA_BASE.Model):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    text = DATA_BASE.Column(DATA_BASE.String(500), nullable=False)
    sender_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    chat_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)

    is_read = DATA_BASE.Column(DATA_BASE.Boolean, default=False)
    timestamp = DATA_BASE.Column(DATA_BASE.DateTime, default=datetime.utcnow)

    def get_time_ago(self):
        if not self.timestamp:
            return ""
        now = datetime.utcnow()
        delta = now - self.timestamp
        
        # Переводим разницу в минуты, часы и дни
        total_seconds = int(delta.total_seconds())
        if total_seconds < 60:
            return "just now"
        
        minutes = total_seconds // 60
        if minutes < 60:
            return f"{minutes}m ago"
            
        hours = minutes // 60
        if hours < 24:
            return f"{hours}h ago"
            
        days = hours // 24
        return f"{days}d ago"



class ChatMember(DATA_BASE.Model):
    __tablename__ = 'chat_members'
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    user_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
    chat_id = DATA_BASE.Column(DATA_BASE.Integer, nullable=False)
