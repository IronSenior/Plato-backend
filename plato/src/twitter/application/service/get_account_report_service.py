from abc import ABC
from ...domain.account.model.account_id import AccountId


class GetAccountReportsService(ABC):

    def getAccountReportsByAccount(self, accountId: AccountId,
                                   afterDate: int, beforeDate: int):
        raise NotImplementedError()
