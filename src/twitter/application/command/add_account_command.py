from commandbus import Command


class AddAccountCommand(Command):

    def __init__(self, accountId: str, brandId: str, name: str,
                 userId: str, oauthToken: str, oauthVerifier: str):
        self.__accountId: str = accountId
        self.__brandId: str = brandId
        self.__name: str = name
        self.__userId: str = userId
        self.__oauthToken: str = oauthToken
        self.__oauthVerifier: str = oauthVerifier

    @property
    def accountId(self):
        return self.__accountId

    @property
    def brandId(self):
        return self.__brandId

    @property
    def name(self):
        return self.__name

    @property
    def userId(self):
        return self.__userId

    @property
    def oauthToken(self):
        return self.__oauthToken

    @property
    def oauthVerifier(self):
        return self.__oauthVerifier
