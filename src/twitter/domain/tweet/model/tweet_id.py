from uuid import UUID


class TweetId():

    def __init__(self, tweetId: UUID):
        self.checkUniqueId(tweetId)
        self.checkIdVersion(tweetId)
        self.__value: UUID = tweetId

    @staticmethod
    def fromString(tweetId: str):
        return TweetId(UUID(tweetId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, tweetId: UUID):
        if type(tweetId) != UUID:
            raise TypeError("Tweet ID must be an UUID instance")

    def checkIdVersion(self, tweetId: UUID):
        if tweetId.version != 4:
            raise TypeError("Tweet ID must be version 4")
