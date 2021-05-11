from ....shared.domain.user_id import UserId
from ...domain.model.brand import Brand
from ..mapper.brand_mapper import BrandMapper
from typing import List, Optional
from ...domain.repository.brands import Brands
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ...application.brand_dto import BrandDTO
from ...application.command.create_brand_command import CreateBrandCommand
from dependency_injector.wiring import inject, Provide


class BrandService:

    @inject
    def __init__(self, brands: Brands = Provide["BRANDS"]):
        self.brands: Brands = brands

    def createBrand(self, brandDto: BrandDTO) -> None:
        PlatoCommandBus.publish(
            CreateBrandCommand(
                id=brandDto["id"],
                userId=brandDto["userid"],
                name=brandDto["name"],
                image=brandDto["image"]
            )
        )

    def getByUserId(self, userid: str) -> Optional[List[Brand]]:
        userId = UserId.fromString(userid)
        brands = self.brands.getByUserId(userId)
        brands_list = list(map(BrandMapper.from_aggregate_to_dto, brands))
        return dict(zip(list(map(lambda brand: brand["id"], brands_list)), brands_list))
