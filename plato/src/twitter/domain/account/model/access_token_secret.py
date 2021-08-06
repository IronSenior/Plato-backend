

class AccessTokenSecret:

    def __init__(self, accessTokenSecret: str):
        self.__value: str = accessTokenSecret

    @staticmethod
    def fromString(accessTokenSecret: str):
        return AccessTokenSecret(accessTokenSecret)

    @property
    def value(self):
        return self.__value
