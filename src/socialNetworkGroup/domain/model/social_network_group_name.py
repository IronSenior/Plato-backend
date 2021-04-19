
class SocialNetworkGroupName:

    def __init__(self, name: str):
        self.__value: str = name

    @staticmethod
    def fromString(name: str):
        return SocialNetworkGroupName(name)

    @property
    def value(self):
        return self.__value
