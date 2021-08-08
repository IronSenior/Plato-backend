from plato_cqrs import Query


class GetAccountQuery(Query):

    def __init__(self, accountId: str):
        self.__accountId: str = accountId

    @property
    def accountId(self):
        return self.__accountId
