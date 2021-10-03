from plato_cqrs import Query


class GetAccountByBrandQuery(Query):

    def __init__(self, brandId: str):
        self.__brandId: str = brandId

    @property
    def brandId(self):
        return self.__brandId
