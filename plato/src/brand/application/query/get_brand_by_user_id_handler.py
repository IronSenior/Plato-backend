from ..brand_dto import BrandDTO
from typing import List
from plato_cqrs import QueryHandler
from .get_brand_by_user_id_query import GetBrandByUserIdQuery
from .get_brand_by_user_id_response import GetBrandByUserIdResponse
from ..service.get_brand_service import GetBrandService
from ....shared.domain.user_id import UserId
from dependency_injector.wiring import inject, Provide
from typing import Optional


class GetBrandByUserIdHandler(QueryHandler):

    @inject
    def __init__(self, getBrandService: GetBrandService = Provide["GET_BRAND_SERVICE"]):
        self.__getBrandService: GetBrandService = getBrandService

    def handle(self, query: GetBrandByUserIdQuery) -> Optional[GetBrandByUserIdResponse]:
        brands: List[BrandDTO] = self.__getBrandService.getBrandByUser(
            UserId.fromString(query.userId)
        )
        getBrandByUserIdResponse = GetBrandByUserIdResponse()
        for brand in brands:
            getBrandByUserIdResponse.addBrand(
                brandId=brand["brandId"],
                userId=brand["userId"],
                name=brand["name"],
                image=brand["image"]
            )
        return getBrandByUserIdResponse
