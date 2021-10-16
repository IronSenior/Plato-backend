from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.tweet.model.tweet import Tweet
import os
import pymongo


@PlatoEventBus.on("TWEET_WAS_PUBLISHED")
def onTweetWasPublished(event: Tweet.TweetWasPublished):
    db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    db["tweets"].update_one(
        {"tweetId": str(event.originator_id)},
        {"$set": {"published": True, "twitterRef": event.twitterRef}}
    )
