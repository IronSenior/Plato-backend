from ...domain.model.brand import Brand
from ...domain.model.brand_id import BrandId
from ...domain.repository.brands import Brands
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional


class BrandRepository(Application, Brands):

    def __init__(self):
        return super(BrandRepository, self).__init__()

    def save(self, brand: Brand) -> None:
        for event in brand.pending_events:
            PlatoEventBus.emit(event.bus_string, event)
        super(BrandRepository, self).save(brand)

    def getById(self, id: BrandId) -> Optional[Brand]:
        try:
            return self.repository.get(id.value)
        except Exception:
            return None
