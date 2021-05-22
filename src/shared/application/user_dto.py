from typing import TypedDict


class UserDTO(TypedDict):
    userid: str
    email: str
    password: str
    username: str
