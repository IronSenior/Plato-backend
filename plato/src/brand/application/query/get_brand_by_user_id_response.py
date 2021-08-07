from plato_cqrs import QueryResponse


class GetBrandByUserIdResponse(QueryResponse):

    def __init__(self, brands: dict = None):
        self.__brands = brands or {}

    @property
    def brands(self) -> list:
        return self.__brands

    def addBrand(self, brandId: str, userId: str, name: str, image: str) -> None:
        self.__brands.update({
            brandId: {
                "userId": userId,
                "name": name,
                "image": image
            }
        })
