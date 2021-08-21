from plato_cqrs import Query


class GetTweetsByAccountQuery(Query):

    def __init__(self, accountId: str, afterDate: float, beforeDate: float):
        self.__accountId: str = accountId
        self.__afterDate: float = afterDate
        self.__beforeDate: float = beforeDate

    @property
    def accountId(self) -> str:
        return self.__accountId

    @property
    def afterDate(self) -> float:
        return self.__afterDate

    @property
    def beforeDate(self) -> float:
        return self.__beforeDate
