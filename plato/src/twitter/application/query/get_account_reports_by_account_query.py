from plato_cqrs import Query


class GetAccountReportsByAccountQuery(Query):

    def __init__(self, accountId: str, afterDate: int, beforeDate: int):
        self.__accountId: str = accountId
        self.__afterDate: int = afterDate
        self.__beforeDate: int = beforeDate

    @property
    def accountId(self) -> str:
        return self.__accountId

    @property
    def afterDate(self) -> int:
        return self.__afterDate

    @property
    def beforeDate(self) -> int:
        return self.__beforeDate
