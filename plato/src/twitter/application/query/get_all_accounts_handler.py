from plato_cqrs import QueryHandler
from .get_all_accounts_query import GetAllAccountsQuery
from .get_accounts_response import GetAccountsResponse
from ..service.get_account_service import GetTwitterAccountService
from dependency_injector.wiring import inject, Provide


class GetAllAccountsHandler(QueryHandler):

    @inject
    def __init__(self, getAccountService: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"]):
        self.__getAccountService: GetTwitterAccountService = getAccountService

    def handle(self, query: GetAllAccountsQuery) -> GetAccountsResponse:
        accounts = self.__getAccountService.getAllAccounts()

        getAccountsResponse = GetAccountsResponse()
        for account in accounts:
            getAccountsResponse.appendAccount(
                accountId=account["accountId"],
                userId=account["userId"],
                brandId=account["brandId"],
                name=account["name"]
            )
        return getAccountsResponse
