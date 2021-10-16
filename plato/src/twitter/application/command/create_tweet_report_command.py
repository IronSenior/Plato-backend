from plato_cqrs import Command


class CreateTweetReportCommand(Command):

    def __init__(self, tweetId: str):
        self.__tweetId: str = tweetId

    @property
    def tweetId(self):
        return self.__tweetId
