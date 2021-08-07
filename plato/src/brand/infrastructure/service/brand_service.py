from typing import List, Optional
from ...domain.repository.brands import Brands
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ....shared.infrastructure.plato_query_bus import PlatoQueryBus
from ...application.brand_dto import BrandDTO
from ...application.command.create_brand_command import CreateBrandCommand
from ...application.query.get_brand_by_user_id_query import GetBrandByUserIdQuery
from ...application.query.get_brand_by_user_id_response import GetBrandByUserIdResponse
from dependency_injector.wiring import inject, Provide


class BrandService:

    @inject
    def __init__(self, brands: Brands = Provide["BRANDS"]):
        self.brands: Brands = brands

    def createBrand(self, brandDto: BrandDTO) -> None:
        PlatoCommandBus.publish(
            CreateBrandCommand(
                id=brandDto["id"],
                userId=brandDto["userId"],
                name=brandDto["name"],
                image=brandDto["image"]
            )
        )

    def getByUserId(self, userId: str) -> Optional[List]:
        brandResponse: GetBrandByUserIdResponse = PlatoQueryBus.publish(GetBrandByUserIdQuery(
            userId=userId
        ))
        if not brandResponse:
            return None
        return brandResponse.brands
