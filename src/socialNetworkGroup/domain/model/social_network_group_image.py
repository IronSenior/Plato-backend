
class SocialNetworkGroupImageUrl:

    def __init__(self, imageurl: str):
        self.__value: str = imageurl

    @staticmethod
    def fromString(imageurl: str):
        return SocialNetworkGroupImageUrl(imageurl)

    @property
    def value(self):
        return self.__value
