from typing import TypedDict


class UserDTO(TypedDict):
    userId: str
    email: str
    password: str
    username: str
