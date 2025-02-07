from typing import Optional
import random


class User:
    def __init__(self, username: str, color_hex: Optional[str] = None, icon_b64: Optional[str] = None) -> None:
        self.username = username

        if color_hex:
            self.color_hex = color_hex
        else:
            # source: https://stackoverflow.com/questions/13998901/generating-a-random-hex-color-in-python
            self.color_hex = "#%06X" % random.randint(0, 0xFFFFFF)

        # icon_b64 can be None.
        self.icon_b64 = icon_b64

    def to_json(self) -> dict[str, Optional[str]]:
        """
        Returns a dictionary representation of the user.
        """
        return {
            "username": self.username,
            "color_hex": self.color_hex,
            "icon_b64": self.icon_b64,
        }

    @classmethod
    def from_json(cls, data: dict[str, Optional[str]]) -> "User":
        """
        Creates a User instance from a JSON dictionary.
        Assumes 'username' is always provided.
        """
        return cls(
            username=data["username"],
            color_hex=data.get("color_hex"),
            icon_b64=data.get("icon_b64")
        )
