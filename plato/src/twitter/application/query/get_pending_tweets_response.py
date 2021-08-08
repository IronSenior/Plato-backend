from plato_cqrs import QueryResponse


class GetPendingTweetsResponse(QueryResponse):

    def __init__(self, tweets: list = None):
        self.__tweets: list = tweets or []

    @property
    def tweets(self):
        return self.__tweets
