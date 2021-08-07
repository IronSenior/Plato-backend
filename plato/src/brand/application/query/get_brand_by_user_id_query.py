from plato_cqrs import Query


class GetBrandByUserIdQuery(Query):

    def __init__(self, userId: str):
        self.__userId: str = userId

    @property
    def userId(self):
        return self.__userId
