from plato_cqrs import QueryHandler

from ...domain.account.model.account_id import AccountId
from dependency_injector.wiring import inject, Provide
from .get_account_reports_by_account_query import GetAccountReportsByAccountQuery
from .get_account_reports_by_account_response import GetAccountReportsByAccountResponse
from ..service.get_account_report_service import GetAccountReportsService


class GetAccountReportsByAccountHandler(QueryHandler):

    @inject
    def __init__(self, getAccountReportsService: GetAccountReportsService = Provide["GET_ACCOUNT_REPORTS_SERVICE"]):
        self.__getAccountReportsService: GetAccountReportsService = getAccountReportsService

    def handle(self, query: GetAccountReportsByAccountQuery) -> GetAccountReportsByAccountResponse:
        reports = self.__getAccountReportsService.getAccountReportsByAccount(
            accountId=AccountId.fromString(query.accountId),
            afterDate=query.afterDate,
            beforeDate=query.beforeDate
        )
        getAccountReportsByAccountResponse = GetAccountReportsByAccountResponse()
        for report in reports:
            getAccountReportsByAccountResponse.appendReport(
                reportId=report["reportId"],
                accountId=report["accountId"],
                reportDate=report["reportDate"],
                followersCount=report["followersCount"],
                friendsCount=report["friendsCount"]
            )
        return getAccountReportsByAccountResponse
