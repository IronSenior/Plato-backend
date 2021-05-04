from commandbus import Command


class CreateBrandCommand(Command):

    def __init__(self, id: str, userId: str, name: str, image: str):
        self.__id = id
        self.__userId = userId
        self.__name = name
        self.__image = image

    @property
    def id(self):
        return self.__id

    @property
    def userId(self):
        return self.__userId

    @property
    def name(self):
        return self.__name

    @property
    def image(self):
        return self.__image
