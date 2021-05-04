from commandbus import Command


class AddAccountCommand(Command):

    def __init__(self, accountId: str, brandId: str, name: str, userId: str, userToken: str, socialNetwork: str):
        self.__accountId: str = accountId
        self.__brandId: str = brandId
        self.__name: str = name
        self.__userId: str = userId
        self.__userToken: str = userToken
        self.__socialNetwork: str = socialNetwork

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
    def userToken(self):
        return self.__userToken

    @property
    def socialNetwork(self):
        return self.__socialNetwork
