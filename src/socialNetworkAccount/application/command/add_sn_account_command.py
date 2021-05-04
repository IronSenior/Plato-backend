from commandbus import Command


class AddSocialNetworkAccountCommand(Command):

    def __init__(self, accountId: str, snGroupId: str, name: str, userId: str, userToken: str, socialNetwork: str):
        self.__accountId: str = accountId
        self.__snGroupId: str = snGroupId
        self.__name: str = name
        self.__userId: str = userId
        self.__userToken: str = userToken
        self.__socialNetwork: str = socialNetwork

    @property
    def accountId(self):
        return self.__accountId

    @property
    def snGroupId(self):
        return self.__snGroupId

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
