from ...domain.model.brand import Brand
from ...domain.model.brand_id import BrandId
from ...domain.repository.brands import Brands
from ....user.domain.model.user_id import UserId
from ....shared.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional, List


class BrandRepository(Application, Brands):

    def __init__(self):
        self.__brands: List[Brand] = []
        return super(BrandRepository, self).__init__()

    def save(self, brand: Brand) -> None:
        super(BrandRepository, self).save(brand)
        self.__brands.append(brand)
        for event in brand.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, id: BrandId) -> Optional[Brand]:
        try:
            return self.repository.get(id.value)
        except Exception:
            return None

    def getByUserId(self, userId: UserId) -> Optional[List[Brand]]:
        brands = []
        for brand in self.__brands:
            if brand.userId == userId.value:
                brands.append(brand)
        return brands
