class UserToken:

    def __init__(self, userToken: str):
        self.__value: str = userToken

    @staticmethod
    def fromString(userToken: str):
        return UserToken(userToken)

    @property
    def value(self):
        return self.__value
