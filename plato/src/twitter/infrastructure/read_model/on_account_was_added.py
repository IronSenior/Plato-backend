from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.account.model.account import Account
import os
import sqlalchemy as db


@PlatoEventBus.on("TWITTER_ACCOUNT_WAS_ADDED")
def onTwitterAccountWasCreated(event: Account.AccountWasAdded):
    engine = db.create_engine(os.environ["DB_ENGINE"])
    connection = engine.connect()
    metadata = db.MetaData()
    accountProjection = db.Table("twitter_accounts", metadata, autoload=True, autoload_with=engine)

    query = db.insert(accountProjection).values(accountid=str(event.originator_id), brandid=event.brandId,
                                                userid=event.userId, name=event.name,
                                                accesstoken=event.accessToken, accesssecret=event.accessTokenSecret)
    connection.execute(query)
