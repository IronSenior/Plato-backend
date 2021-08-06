class AccessToken:

    def __init__(self, accessToken: str):
        self.__value: str = accessToken

    @staticmethod
    def fromString(accessToken: str):
        return AccessToken(accessToken)

    @property
    def value(self):
        return self.__value
