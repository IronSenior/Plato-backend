from uuid import UUID


class AccountId():

    def __init__(self, accountId: UUID):
        self.checkUniqueId(accountId)
        self.checkIdVersion(accountId)
        self.__value: UUID = accountId

    @staticmethod
    def fromString(accountId: str):
        return AccountId(UUID(accountId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, accountId: UUID):
        if type(accountId) != UUID:
            raise TypeError("Account ID must be an UUID instance")

    def checkIdVersion(self, accountId: UUID):
        if accountId.version != 4:
            raise TypeError("Account ID must be version 4")
