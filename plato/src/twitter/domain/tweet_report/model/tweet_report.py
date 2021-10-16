from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from ...tweet.model.tweet_id import TweetId
from .report_id import ReportId
from datetime import datetime


class TweetReport(Aggregate):

    def __init__(self, tweetId: TweetId, reportDate: int, retweetCount: int,
                 favCount: int, quoteCount: int, replyCount: int, *args, **kwargs):
        super(TweetReport, self).__init__(*args, **kwargs)
        self._tweetId: TweetId = tweetId
        self._reportDate: datetime = reportDate
        self._retweetCount: int = retweetCount
        self._facCount: int = favCount
        self._quoteCount: int = quoteCount
        self._replyCount: int = replyCount

    @property
    def tokenId(self):
        return self._id

    @property
    def tweetId(self):
        return self._tweetId

    @property
    def reportDate(self):
        return self._reportDate

    @property
    def retweetCount(self):
        return self._retweetCount

    @property
    def favCount(self):
        return self._favCount

    @property
    def quoteCount(self):
        return self._quoteCount

    @property
    def replyCount(self):
        return self._replyCount

    @classmethod
    def add(cls, reportId: ReportId, tweetId: TweetId, reportDate: datetime,
            retweetCount: int, favCount: int, quoteCount: int, replyCount: int):
        return cls._create(
            cls.TweetReportWasCreated,
            id=reportId.value,
            tweetId=str(tweetId.value),
            reportDate=reportDate.timestamp(),
            retweetCount=retweetCount,
            favCount=favCount,
            quoteCount=quoteCount,
            replyCount=replyCount
        )

    class TweetReportWasCreated(AggregateCreated):
        bus_string = "TWEET_REPORT_WAS_CREATED"
        tweetId: str
        reportDate: float
        retweetCount: int
        favCount: int
        quoteCount: int
        replyCount: int

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            report = super().mutate(obj)
            report._tweetId = self.tweetId
            report._reportDate = datetime.fromtimestamp(self.reportDate)
            report._retweetCount = self.retweetCount
            report._favCount = self.favCount
            report._quoteCount = self.quoteCount
            report._replyCount = self.replyCount
            return report
