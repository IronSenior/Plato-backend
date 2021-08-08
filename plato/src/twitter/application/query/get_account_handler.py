from plato_cqrs import QueryHandler
from dependency_injector.wiring import Provide, inject
from ...domain.account.repository.accounts import Accounts
from ...domain.account.model.account_id import AccountId
from .get_account_query import GetAccountQuery
from .get_account_response import GetAccountResponse


class GetAccountHandler(QueryHandler):

    @inject
    def __init__(self, accounts: Accounts = Provide["TWITTER_ACCOUNTS"]):
        self.__accounts: Accounts = accounts

    def handle(self, query: GetAccountQuery) -> GetAccountResponse:
        accountId = AccountId.fromString(query.accountId)
        account = self.__accounts.getById(accountId)

        if not account:
            return None

        return GetAccountResponse(
            accountId=str(account.accountId),
            userId=account.userId,
            brandId=account.userId,
            name=account.name,
            accessToken=account.accessToken,
            accessTokenSecret=account.accessTokenSecret
        )
