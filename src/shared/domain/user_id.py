from uuid import UUID


class UserId():

    def __init__(self, userId: UUID):
        self.checkUniqueId(userId)
        self.checkIdVersion(userId)
        self.__value: UUID = userId

    @staticmethod
    def fromString(userId: str):
        return UserId(UUID(userId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, userId: UUID):
        if type(userId) != UUID:
            raise TypeError("User ID must be an UUID instance")

    def checkIdVersion(self, userId: UUID):
        if userId.version != 4:
            raise TypeError("User ID must be version 4")
