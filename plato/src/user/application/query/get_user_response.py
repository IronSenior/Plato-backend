from plato_cqrs import QueryResponse


class GetUserResponse(QueryResponse):

    def __init__(self, userId: str, username: str, usermail: str, password: str):
        self.__userId: str = userId
        self.__username: str = username
        self.__usermail: str = usermail
        self.__password: str = password

    @property
    def userId(self):
        return self.__userId

    @property
    def username(self):
        return self.__username

    @property
    def usermail(self):
        return self.__usermail

    @property
    def password(self):
        return self.__password

    @property
    def userDto(self):
        return {
            "userId": self.__userId,
            "username": self.__username,
            "usermail": self.__usermail,
            "password": self.__password
        }
