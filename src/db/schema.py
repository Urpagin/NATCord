import datetime
import random
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = "users"  # Static table name for users
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Optional attributes for customization
    color_hex = db.Column(db.String(7), nullable=False, default="#%06X" % random.randint(0, 0xFFFFFF))
    icon_b64 = db.Column(db.Text, nullable=True)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now)

    # Relationship: one user may have many messages
    messages = db.relationship('Message', backref='sender', lazy=True)

    def set_password(self, password: str) -> None:
        """Generate and store the password hash."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check a provided password against the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_json(self) -> dict:
        """Serialize the User model to JSON-compatible dict."""
        return {
            "id": self.id,
            "username": self.username,
            "color_hex": self.color_hex,
            "icon_b64": self.icon_b64,
            "creation_time": self.creation_time.isoformat()
        }

class Message(db.Model):
    __tablename__ = "messages"  # Static table name for messages
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def to_json(self) -> dict:
        """Serialize the Message model to JSON-compatible dict."""
        return {
            "id": self.id,
            "sender": self.sender.to_json() if self.sender else None,
            "content": self.content,
            "timestamp": int(self.timestamp.timestamp()),
            "uuid": self.uuid
        }
