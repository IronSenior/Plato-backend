from ...domain.tweet.repository.tweets import Tweets
from ...domain.tweet.model.tweet import Tweet
from ...domain.tweet.model.tweet_id import TweetId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional


class TweetRepository(Application, Tweets):

    def __init__(self):
        return super(TweetRepository, self).__init__()

    def save(self, tweet: Tweet):
        for event in tweet.pending_events:
            PlatoEventBus.emit(event.bus_string, event)
        super(TweetRepository, self).save(tweet)

    def getById(self, tweetId: TweetId) -> Optional[Tweet]:
        try:
            return self.repository.get(tweetId.value)
        except Exception:
            return None
