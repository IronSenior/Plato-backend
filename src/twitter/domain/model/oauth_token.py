class OauthToken:

    def __init__(self, oauthToken: str):
        self.__value: str = oauthToken

    @staticmethod
    def fromString(oauthToken: str):
        return OauthToken(oauthToken)

    @property
    def value(self):
        return self.__value
