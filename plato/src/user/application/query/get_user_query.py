from plato_cqrs import Query


class GetUserQuery(Query):

    def __init__(self, userId: str):
        self.__userId: str = userId

    @property
    def userId(self):
        return self.__userId
