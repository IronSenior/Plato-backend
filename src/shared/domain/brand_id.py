from uuid import UUID


class BrandId:

    def __init__(self, brandId: UUID):
        self.checkUniqueId(brandId)
        self.checkIdVersion(brandId)
        self.__value: UUID = brandId

    @staticmethod
    def fromString(brandId: str):
        return BrandId(UUID(brandId))

    @property
    def value(self):
        return self.__value

    def checkUniqueId(self, brandId: UUID):
        if type(brandId) != UUID:
            raise TypeError("User ID must be an UUID instance")

    def checkIdVersion(self, brandId: UUID):
        if brandId.version != 4:
            raise TypeError("User ID must be version 4")
