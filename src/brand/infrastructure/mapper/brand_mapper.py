

from ...application.brand_dto import BrandDTO
from ...domain.model.brand import Brand


class BrandMapper:

    @staticmethod
    def from_aggregate_to_dto(brand: Brand):
        return BrandDTO(
            id=str(brand.id),
            userid=str(brand.userId),
            name=brand.name,
            image=brand.image
        )
