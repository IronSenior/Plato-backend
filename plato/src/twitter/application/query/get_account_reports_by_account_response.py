from plato_cqrs import QueryResponse


class GetAccountReportsByAccountResponse(QueryResponse):

    def __init__(self, reports: list = None):
        self.__reports: list = reports or []

    @property
    def reports(self):
        return self.__reports

    def appendReport(self, reportId: str, accountId: str, reportDate: int,
                     followersCount: int, friendsCount: int):
        self.__reports.append({
            "reportId": reportId,
            "accountId": accountId,
            "reportDate": reportDate,
            "followersCount": followersCount,
            "friendsCount": friendsCount
        })
