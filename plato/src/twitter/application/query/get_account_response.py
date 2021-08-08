from plato_cqrs import QueryResponse


class GetAccountResponse(QueryResponse):

    def __init__(self, accountId: str, userId: str, brandId: str,
                 name: str, accessToken: str, accessTokenSecret: str):
        self.__accountId: str = accountId
        self.__userId: str = userId
        self.__brandId: str = brandId
        self.__name: str = name
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
    def accessToken(self):
        return self.__accessToken

    @property
    def accessTokenSecret(self):
        return self.__accessTokenSecret

    @property
    def userId(self):
        return self.__userId
