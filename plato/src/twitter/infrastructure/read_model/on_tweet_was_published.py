from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.tweet.model.tweet import Tweet
import sqlalchemy as db
import os


@PlatoEventBus.on("TWEET_WAS_PUBLISHED")
def onTweetWasPublished(event: Tweet.TweetWasPublished):
    engine = db.create_engine(os.environ["DB_ENGINE"])
    connection = engine.connect()
    metadata = db.MetaData()
    tweetsProjection = db.Table("pending_tweets", metadata, autoload=True, autoload_with=engine)

    query = db.update(tweetsProjection
                      ).values(published=True
                               ).where(tweetsProjection.columns.tweetid == str(event.originator_id))
    connection.execute(query)
