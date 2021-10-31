from datetime import datetime
from eventsourcing.domain import Aggregate, AggregateCreated, AggregateEvent
from ...account.model.account_id import AccountId
from .tweet_description import TweetDescription
from .tweet_id import TweetId
from typing import Optional


class Tweet(Aggregate):

    def __init__(self, accountId: AccountId, publicationDate: datetime,
                 description: TweetDescription, published: bool = False,
                 twitterRef: str = "", media: list = [], *args, **kwargs):
        super(Tweet, self).__init__(*args, **kwargs)
        self._accountId: AccountId = accountId
        self._description: TweetDescription = description
        self._publicationDate: datetime = publicationDate
        self._published: bool = published
        self._twitterRef: str = twitterRef
        self._media: list = media

    @property
    def id(self):
        return self._id

    @property
    def accountId(self):
        return self._accountId.value

    @property
    def description(self):
        return self._description.value

    @property
    def publicationDate(self):
        return self._publicationDate

    @property
    def published(self):
        return self._published

    @property
    def twitterRef(self):
        return self._twitterRef

    @property
    def media(self):
        return self._media

    @classmethod
    def add(cls, tweetId: TweetId, accountId: AccountId,
            description: TweetDescription, publicationDate: datetime):
        return cls._create(
            cls.TweetWasScheduled,
            id=tweetId.value,
            accountId=str(accountId.value),
            description=description.value,
            publicationDate=int(publicationDate.timestamp() * 1000)
        )

    class TweetWasScheduled(AggregateCreated):
        bus_string = "TWEET_WAS_SCHEDULED"
        accountId: str
        description: str
        publicationDate: int

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            tweet = super().mutate(obj)
            tweet._description = TweetDescription.fromString(self.description)
            tweet._accountId = AccountId.fromString(self.accountId)
            tweet._publicationDate = datetime.fromtimestamp(self.publicationDate / 1000)
            return tweet

    def publish(self, twitterRef: str):
        return self.trigger_event(
            self.TweetWasPublished,
            twitterRef=twitterRef
        )

    class TweetWasPublished(AggregateEvent):
        bus_string = "TWEET_WAS_PUBLISHED"
        twitterRef: str

        def apply(self, aggregate: Aggregate) -> None:
            aggregate._published = True
            aggregate._twitterRef = self.twitterRef

    def addMedia(self, media: str):
        return self.trigger_event(
            self.TweetMediaWasAdded,
            media=media
        )

    class TweetMediaWasAdded(AggregateEvent):
        bus_string = "TWEET_MEDIA_WAS_ADDED"
        media: str

        def apply(self, aggregate: Aggregate) -> None:
            aggregate._media.append(self.media)
