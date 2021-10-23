from datetime import datetime
import uuid

from ..account_dto import AccountDTO
from .create_account_report_command import CreateAccountReportCommand
from ...domain.account_report.repository.account_reports import AccountReports
from ...domain.account.model.account_id import AccountId
from ...domain.account_report.model.account_report import AccountReport
from ..account_status_dto import AccountStatusDTO
from ..service.get_account_service import GetTwitterAccountService
from ...domain.account_report.service.account_status_retriever import AccountStatusRetriever
from dependency_injector.wiring import Provide, inject
from plato_cqrs import CommandHandler


class CreateAccountReportHandler(CommandHandler):

    @inject
    def __init__(self, accountReports: AccountReports = Provide["ACCOUNT_REPORTS"],
                 getAccountService: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"],
                 accountStatusRetriever: AccountStatusRetriever = Provide["ACCOUNT_STATUS_RETRIEVER"]):
        self.__accountReports: AccountReports = accountReports
        self.__accountStatusRetriever: AccountStatusRetriever = accountStatusRetriever
        self.__getAccountService: GetTwitterAccountService = getAccountService

    def handle(self, cmd: CreateAccountReportCommand):
        accountId: AccountId = AccountId.fromString(cmd.accountId)
        account: AccountDTO = self.__getAccountService.getAccountById(accountId)

        accountStatus: AccountStatusDTO = self.__accountStatusRetriever.withAccount(account)

        if not accountStatus:
            return None

        reportId = AccountId(uuid.uuid4())
        report: AccountReport = AccountReport.add(
            reportId=reportId,
            accountId=accountId,
            reportDate=datetime.now(),
            followersCount=accountStatus["followers_count"],
            friendsCount=accountStatus["friends_count"]
        )
        self.__accountReports.save(report)
