
class SocialNetworkAccountName:

    def __init__(self, name: str):
        self.__value: str = name

    @staticmethod
    def fromString(name: str):
        return SocialNetworkAccountName(name)

    @property
    def value(self):
        return self.__value
