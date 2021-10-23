from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from ...account.model.account_id import AccountId
from .report_id import ReportId
from datetime import datetime


class AccountReport(Aggregate):

    def __init__(self, accountId: AccountId, reportDate: datetime, followersCount: int,
                 friendsCount: int, *args, **kwargs):
        super(AccountReport, self).__init__(*args, **kwargs)
        self._accountId: AccountId = accountId
        self._reportDate: datetime = reportDate
        self._followersCount: int = followersCount
        self._friendsCount: int = friendsCount

    @property
    def reportId(self):
        return self._id

    @property
    def accountId(self):
        return self._accountId

    @property
    def reportDate(self):
        return self._reportDate

    @property
    def followersCount(self):
        return self._retweetCount

    @property
    def friendsCount(self):
        return self._friendsCount

    @classmethod
    def add(cls, reportId: ReportId, accountId: AccountId, reportDate: datetime,
            followersCount: int, friendsCount: int):
        return cls._create(
            cls.AccountReportWasCreated,
            id=reportId.value,
            accountId=str(accountId.value),
            reportDate=int(reportDate.timestamp() * 1000),
            followersCount=followersCount,
            friendsCount=friendsCount
        )

    class AccountReportWasCreated(AggregateCreated):
        bus_string = "ACCOUNT_REPORT_WAS_CREATED"
        accountId: str
        reportDate: int
        followersCount: int
        friendsCount: int

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            report = super().mutate(obj)
            report._accountId = self.accountId
            report._reportDate = datetime.fromtimestamp(self.reportDate / 1000)
            report._followersCount = self.followersCount
            report._friendsCount = self.friendsCount
            return report
