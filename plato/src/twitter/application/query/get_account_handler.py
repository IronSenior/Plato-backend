from plato_cqrs import QueryHandler
from .get_account_query import GetAccountQuery
from .get_account_response import GetAccountResponse
from ...domain.account.model.account_id import AccountId
from ..service.get_account_service import GetTwitterAccountService
from dependency_injector.wiring import inject, Provide


class GetAccountHandler(QueryHandler):

    @inject
    def __init__(self, getAccountService: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"]):
        self.__getAccountService: GetTwitterAccountService = getAccountService

    def handle(self, query: GetAccountQuery) -> GetAccountResponse:
        account = self.__getAccountService.getAccountById(
            AccountId.fromString(query.accountId)
        )

        return GetAccountResponse(
            accountId=account["accountId"],
            brandId=account["brandId"],
            userId=account["userId"],
            name=account["name"],
            accessToken=account["accessToken"],
            accessTokenSecret=account["accessSecret"]
        )
