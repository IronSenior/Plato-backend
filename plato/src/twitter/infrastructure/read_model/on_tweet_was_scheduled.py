from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.tweet.model.tweet import Tweet
import os
import sqlalchemy as db


@PlatoEventBus.on("TWEET_WAS_SCHEDULED")
def onTweetWasScheduled(event: Tweet.TweetWasScheduled):
    engine = db.create_engine(os.environ["DB_ENGINE"])
    connection = engine.connect()
    metadata = db.MetaData()
    tweetsProjection = db.Table("pending_tweets", metadata, autoload=True, autoload_with=engine)

    query = db.insert(tweetsProjection).values(tweetid=str(event.originator_id), accountid=event.accountId,
                                               description=event.description, publicationdate=event.publicationDate,
                                               published=False)
    connection.execute(query)
