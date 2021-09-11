from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.model.brand import Brand
import os
import pymongo
from pymongo.collection import Collection


@PlatoEventBus.on("BRAND_WAS_CREATED")
def onBrandWasCreated(event: Brand.BrandWasCreated):
    client = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    brandProjection: Collection = client["brands"]
    brandProjection.insert_one({
        "brandId": str(event.originator_id),
        "userId": event.userId,
        "name": event.name,
        "image": event.image
    })
