from plato_cqrs import QueryResponse


class GetTweetsByAccountResponse(QueryResponse):

    def __init__(self, tweets: list = None):
        self.__tweets: list = tweets or []

    @property
    def tweets(self):
        return self.__tweets

    def appendTweet(self, tweetId: str, accountId: str, description: str,
                    publicationDate: int, published: bool):
        self.__tweets.append({
            "tweetId": tweetId,
            "accountId": accountId,
            "description": description,
            "publicationDate": publicationDate,
            "published": published
        })
