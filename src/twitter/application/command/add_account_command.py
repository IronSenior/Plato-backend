from plato_cqrs import Command


class AddAccountCommand(Command):

    def __init__(self, accountId: str, brandId: str, name: str,
                 userId: str, accessToken: str, accessTokenSecret: str):
        self.__accountId: str = accountId
        self.__brandId: str = brandId
        self.__name: str = name
        self.__userId: str = userId
        self.__accessToken: str = accessToken
        self.__accessTokenSecret: str = accessTokenSecret

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
    def accessToken(self):
        return self.__accessToken

    @property
    def accessTokenSecret(self):
        return self.__accessTokenSecret
