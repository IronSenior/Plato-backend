from datetime import datetime
from eventsourcing.domain import Aggregate, AggregateCreated, AggregateEvent
from ...account.model.account_id import AccountId
from .tweet_description import TweetDescription
from .tweet_id import TweetId
from typing import Optional


class Tweet(Aggregate):

    def __init__(self, accountId: AccountId, publicationDate: datetime,
                 description: TweetDescription, published: bool = False, *args, **kwargs):
        super(Tweet, self).__init__(*args, **kwargs)
        self._accountId: AccountId = accountId
        self._description: TweetDescription = description
        self._publicationDate: datetime = publicationDate
        self._published: bool = published

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

    @classmethod
    def add(cls, tweetId: TweetId, accountId: AccountId,
            description: TweetDescription, publicationDate: datetime):
        return cls._create(
            cls.TweetWasScheduled,
            id=tweetId.value,
            accountId=str(accountId.value),
            description=description.value,
            publicationDate=publicationDate.timestamp()
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
            tweet._publicationDate = datetime.fromtimestamp(self.publicationDate)
            return tweet

    def publish(self):
        return self.trigger_event(
            self.TweetWasPublished
        )

    class TweetWasPublished(AggregateEvent):
        bus_string = "TWEET_WAS_PUBLISHED"

        def apply(self, aggregate: Aggregate) -> None:
            aggregate._published = True
