from datetime import datetime
from ...domain.tweet.repository.tweets import Tweets
from ...domain.tweet.model.tweet import Tweet
from ...domain.account.model.account_id import AccountId
from ...domain.tweet.model.tweet_id import TweetId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import List, Optional


class MemoryTweetRepository(Application, Tweets):

    def __init__(self):
        self.__tweets: List[Tweet] = []
        return super(MemoryTweetRepository, self).__init__()

    def save(self, tweet: Tweet):
        super(MemoryTweetRepository, self).save(tweet)
        self.__tweets.append(tweet)
        for event in tweet.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, tweetId: TweetId) -> Optional[Tweet]:
        try:
            return self.repository.get(tweetId.value)
        except Exception:
            return None

    def getByAccountId(self, accountId: AccountId) -> Optional[List[Tweet]]:
        tweets = filter(self.__tweets,
                        lambda tweet: tweet.accountId == accountId.value)
        return tweets

    def getPendingTweets(self) -> Optional[List[Tweet]]:
        print("ESTOY EN EL REPO")
        print(self.__tweets)
        tweets = list(filter(lambda tweet: tweet.publicationDate <= datetime.now(), self.__tweets))
        print(tweets)
        return tweets
