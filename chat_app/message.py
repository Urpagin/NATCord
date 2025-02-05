from uuid import uuid4
import time

class Message:
    """Class for representing a very simple message"""

    def __init__(self, content: str):
        self.content = content
        self.uuid = str(uuid4())  # Convert UUID to string
        self.timestamp = int(time.time())  # Store timestamp as integer

    def __repr__(self):
        return f"Message(content={self.content}, uuid={self.uuid}, timestamp={self.timestamp})"

