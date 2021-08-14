from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.model.brand import Brand
import os
import sqlalchemy as db


@PlatoEventBus.on("BRAND_WAS_CREATED")
def onBrandWasCreated(event: Brand.BrandWasCreated):
    engine = db.create_engine(os.environ["DB_ENGINE"])
    connection = engine.connect()
    metadata = db.MetaData()
    brandProjection = db.Table("brands", metadata, autoload=True, autoload_with=engine)

    query = db.insert(brandProjection).values(brandid=str(event.originator_id), userid=event.userId,
                                              name=event.name, image=event.image)
    connection.execute(query)
