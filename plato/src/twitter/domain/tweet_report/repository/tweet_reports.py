
from abc import ABC
from typing import Optional
from ..model.report_id import ReportId
from ..model.tweet_report import TweetReport


class TweetReports(ABC):

    def save(self, report: TweetReport) -> None:
        raise NotImplementedError

    def getById(self, reportId: ReportId) -> Optional[TweetReport]:
        raise NotImplementedError
