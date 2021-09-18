from typing import TypedDict


class UserDTO(TypedDict):
    userId: str
    usermail: str
    password: str
    username: str
