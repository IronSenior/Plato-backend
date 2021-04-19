from uuid import UUID


class SocialNetworkGroupId:

    def __init__(self, socialNetworkGroupId: UUID):
        self.checkUniqueId(socialNetworkGroupId)
        self.checkIdVersion(socialNetworkGroupId)
        self.__value: UUID = socialNetworkGroupId

    @staticmethod
    def fromString(socialNetworkGroupId: str):
        return SocialNetworkGroupId(UUID(socialNetworkGroupId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, socialNetworkGroupId: UUID):
        if type(socialNetworkGroupId) != UUID:
            raise TypeError("User ID must be an UUID instance")

    def checkIdVersion(self, socialNetworkGroupId: UUID):
        if socialNetworkGroupId.version != 4:
            raise TypeError("User ID must be version 4")
