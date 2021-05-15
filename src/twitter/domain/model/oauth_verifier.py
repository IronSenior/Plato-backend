

class OauthVerifier:

    def __init__(self, oauthVerifier: str):
        self.__value: str = oauthVerifier

    @staticmethod
    def fromString(oauthVerifier: str):
        return OauthVerifier(oauthVerifier)

    @property
    def value(self):
        return self.__value
