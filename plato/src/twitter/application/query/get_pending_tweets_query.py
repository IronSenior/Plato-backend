from plato_cqrs import Query


class GetPendingTweetsQuery(Query):

    def __init__(self, publicationDate: float):
        self.__publicationDate: float = publicationDate

    @property
    def publicationDate(self) -> float:
        return self.__publicationDate
