from uuid import uuid4
import time
from typing import Optional
from src.user import User

class Message:
    """Class for representing a very simple message."""

    def __init__(self, user: User, content: str, timestamp: int | None = None, uuid: str | None = None):
        assert isinstance(user, User), f"Wrong type for user. Got {type(user)}"
                    
        self.user: User = user
        self.content = content
        self.uuid = uuid if uuid else str(uuid4())
        self.timestamp = timestamp if timestamp else int(time.time())

    def __repr__(self):
        # !r conversion flag to ensure that strings are shown in their quoted form.
        return (f"Message(user={self.user!r}, content={self.content!r}, "
                f"uuid={self.uuid!r}, timestamp={self.timestamp})")
    
    def to_json(self) -> dict:
        """
        Returns a dict ready to be used on the network.
        """
        return {
            'user': self.user.to_json(),
            'content': self.content,
            'uuid': self.uuid,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_json(cls, message: dict[str, str | int]) -> "Message":
        """
        Parses a `Message` from a JSON dict.
        """
        # Create an instance using provided user, content, and timestamp.
        instance = cls(
            user=User.from_json(message['user']),
            content=message['content'],
            timestamp=message.get('timestamp')
        )
        # Override the auto-generated uuid if one is provided.
        instance.uuid = message.get('uuid', instance.uuid)
        return instance
