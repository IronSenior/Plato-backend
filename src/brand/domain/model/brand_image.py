
class BrandImageUrl:

    def __init__(self, imageUrl: str):
        self.__value: str = imageUrl

    @staticmethod
    def fromString(imageUrl: str):
        return BrandImageUrl(imageUrl)

    @property
    def value(self):
        return self.__value
