
class BrandName:

    def __init__(self, name: str):
        self.__value: str = name

    @staticmethod
    def fromString(name: str):
        return BrandName(name)

    @property
    def value(self):
        return self.__value
