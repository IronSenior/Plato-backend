from plato_cqrs import Command


class ScheduleTweetCommand(Command):

    def __init__(self, tweetId: str, accountId: str, description: str, publicationDate: int):
        self.__tweetId: str = tweetId
        self.__accountId: str = accountId
        self.__description: str = description
        self.__publicationDate: int = publicationDate

    @property
    def tweetId(self):
        return self.__tweetId

    @property
    def accountId(self):
        return self.__accountId

    @property
    def description(self):
        return self.__description

    @property
    def publicationDate(self):
        return self.__publicationDate
