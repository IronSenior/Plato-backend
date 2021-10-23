
from abc import ABC
from typing import Optional
from ..model.report_id import ReportId
from ..model.account_report import AccountReport


class AccountReports(ABC):

    def save(self, report: AccountReport) -> None:
        raise NotImplementedError

    def getById(self, reportId: ReportId) -> Optional[AccountReport]:
        raise NotImplementedError
