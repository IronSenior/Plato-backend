from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.account.model.account import Account
import pymongo
import os


@PlatoEventBus.on("TWITTER_ACCOUNT_WAS_ADDED")
def onTwitterAccountWasCreated(event: Account.AccountWasAdded):
    db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    accountDTO = {
        "accountId": str(event.originator_id),
        "brandId": event.brandId,
        "userId": event.userId,
        "name": event.name,
        "accessToken": event.accessToken,
        "accessSecret": event.accessTokenSecret
    }
    twitterProjection = db["twitter_accounts"]
    twitterProjection.insert_one(accountDTO)
