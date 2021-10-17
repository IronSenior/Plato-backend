from plato_cqrs import Query


class GetTweetQuery(Query):

    def __init__(self, tweetId: str):
        self.__tweetId: str = tweetId

    @property
    def tweetId(self) -> str:
        return self.__tweetId
