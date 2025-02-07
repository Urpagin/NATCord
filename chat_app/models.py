from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from os import getenv
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()



class User(UserMixin, db.Model):
    __tablename__ = getenv("user_table", "User")
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_premium = db.Column(db.Boolean, default=False, nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now)

    messages = db.relationship('Message', backref='sender', lazy=True)
    memberships = db.relationship('Member', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Friend(db.Model):
    __tablename__ = getenv("friendship_table", "Friend")
    id = db.Column(db.Integer, primary_key=True)
    id_user1 = db.Column(db.Integer, db.ForeignKey(f'{getenv("user_table", "User")}.id'), nullable=False)
    id_user2 = db.Column(db.Integer, db.ForeignKey(f'{getenv("user_table", "User")}.id'), nullable=False)

class Server(db.Model):
    __tablename__ = getenv("server_table", "Server")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Channel(db.Model):
    __tablename__ = getenv("channel_table", "Channel")
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey(f'{getenv("server_table", "Server")}.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class ConversationParticipant(db.Model):
    __tablename__ = getenv("conversation_participant_table", "Conversation_participant")
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{getenv("user_table", "User")}.id'), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey(f'{getenv("conversation_table", "Conversation")}.id'), nullable=False)

class Conversation(db.Model):
    __tablename__ = getenv("conversation_table", "Conversation")
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey(f'{getenv("channel_table", "Channel")}.id'), nullable=False)

class Message(db.Model):
    __tablename__ = getenv("message_table", "Message")
    id = db.Column(db.Integer, primary_key=True)
    id_chat = db.Column(db.Integer, db.ForeignKey(f'{getenv("conversation_table", "Conversation")}.id'), nullable=False)
    id_sender = db.Column(db.Integer, db.ForeignKey(f'{getenv("user_table", "User")}.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

class File(db.Model):
    __tablename__ = getenv("file_table", "File")
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey(f'{getenv("message_table", "Message")}.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
