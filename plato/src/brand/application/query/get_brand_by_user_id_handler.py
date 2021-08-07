from plato_cqrs import QueryHandler
from ...domain.repository.brands import Brands
from ...domain.model.brand import Brand
from ....shared.domain.user_id import UserId
from .get_brand_by_user_id_query import GetBrandByUserIdQuery
from .get_brand_by_user_id_response import GetBrandByUserIdResponse
from dependency_injector.wiring import inject, Provide
from typing import Optional


class GetBrandByUserIdHandler(QueryHandler):

    @inject
    def __init__(self, brands: Brands = Provide["BRANDS"]):
        self.__brands: Brands = brands

    def handle(self, query: GetBrandByUserIdQuery) -> Optional[GetBrandByUserIdResponse]:
        userId = UserId.fromString(query.userId)

        userBrands: list[Brand] = self.__brands.getByUserId(userId)

        if not userBrands:
            return None

        getBrandByUserIdResponse = GetBrandByUserIdResponse()
        for brand in userBrands:
            getBrandByUserIdResponse.addBrand(
                brandId=str(brand.id),
                userId=brand.userId,
                name=brand.name,
                image=brand.image
            )

        return getBrandByUserIdResponse
