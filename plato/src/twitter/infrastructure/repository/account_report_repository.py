from ...domain.account_report.repository.account_reports import AccountReports
from ...domain.account_report.model.account_report import AccountReport
from ...domain.account_report.model.report_id import ReportId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional


class AccountReportRepository(Application, AccountReports):

    def __init__(self):
        return super(AccountReportRepository, self).__init__()

    def save(self, report: AccountReport):
        for event in report.pending_events:
            PlatoEventBus.emit(event.bus_string, event)
        super(AccountReportRepository, self).save(report)

    def getById(self, reportId: ReportId) -> Optional[AccountReport]:
        try:
            return self.repository.get(reportId.value)
        except Exception:
            return None
