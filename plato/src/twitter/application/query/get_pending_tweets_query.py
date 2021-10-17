from plato_cqrs import Query


class GetPendingTweetsQuery(Query):

    def __init__(self, publicationDate: int):
        self.__publicationDate: int = publicationDate

    @property
    def publicationDate(self) -> int:
        return self.__publicationDate
