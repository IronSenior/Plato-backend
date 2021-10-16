from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.tweet.model.tweet import Tweet
import pymongo
import os


@PlatoEventBus.on("TWEET_WAS_SCHEDULED")
def onTweetWasScheduled(event: Tweet.TweetWasScheduled):
    db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    tweetDTO = {
        "tweetId": str(event.originator_id),
        "accountId": event.accountId,
        "description": event.description,
        "publicationDate": event.publicationDate,
        "published": False,
        "twitterRef": "",
    }
    db["tweets"].insert_one(tweetDTO)
