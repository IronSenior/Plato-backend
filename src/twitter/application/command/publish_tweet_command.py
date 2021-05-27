from simpleCQRS import Command


class PublishTweetCommand(Command):

    def __init__(self, tweetId: str):
        self.__tweetId: str = tweetId

    @property
    def tweetId(self):
        return self.__tweetId
