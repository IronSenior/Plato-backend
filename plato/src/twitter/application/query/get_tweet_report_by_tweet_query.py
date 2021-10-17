from plato_cqrs import Query


class GetTweetReportsByTweetQuery(Query):

    def __init__(self, tweetId: str, afterDate: int, beforeDate: int):
        self.__tweetId: str = tweetId
        self.__afterDate: int = afterDate
        self.__beforeDate: int = beforeDate

    @property
    def tweetId(self) -> str:
        return self.__tweetId

    @property
    def afterDate(self) -> int:
        return self.__afterDate

    @property
    def beforeDate(self) -> int:
        return self.__beforeDate
