from plato_cqrs import Command


class AddTweetMediaCommand(Command):

    def __init__(self, tweetId: str, media: str):
        self.__tweetId: str = tweetId
        self.__media: str = media

    @property
    def tweetId(self):
        return self.__tweetId

    @property
    def media(self):
        return self.__media
