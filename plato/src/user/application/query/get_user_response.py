from plato_cqrs import QueryResponse


class GetUserResponse(QueryResponse):

    def __init__(self, userId: str, username: str, email: str, password: str):
        self.__userId: str = userId
        self.__username: str = username
        self.__email: str = email
        self.__password: str = password

    @property
    def userId(self):
        return self.__userId

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @property
    def userDto(self):
        return {
            "userId": self.__userId,
            "username": self.__username,
            "email": self.__email,
            "password": self.__password
        }
