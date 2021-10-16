from ...domain.tweet_report.repository.tweet_reports import TweetReports
from ...domain.tweet_report.model.tweet_report import TweetReport
from ...domain.tweet_report.model.report_id import ReportId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional


class TweetReportRepository(Application, TweetReports):

    def __init__(self):
        return super(TweetReportRepository, self).__init__()

    def save(self, report: TweetReport):
        for event in report.pending_events:
            PlatoEventBus.emit(event.bus_string, event)
        super(TweetReportRepository, self).save(report)

    def getById(self, reportId: ReportId) -> Optional[TweetReport]:
        try:
            return self.repository.get(reportId.value)
        except Exception:
            return None
