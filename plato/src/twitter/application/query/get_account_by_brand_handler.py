from plato_cqrs import QueryHandler
from .get_account_by_brand_query import GetAccountByBrandQuery
from .get_account_response import GetAccountResponse
from ....shared.domain.brand_id import BrandId
from ..service.get_account_service import GetTwitterAccountService
from dependency_injector.wiring import inject, Provide


class GetAccountByBrandHandler(QueryHandler):

    @inject
    def __init__(self, getAccountService: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"]):
        self.__getAccountService: GetTwitterAccountService = getAccountService

    def handle(self, query: GetAccountByBrandQuery) -> GetAccountResponse:
        account = self.__getAccountService.getAccountByBrandId(
            BrandId.fromString(query.brandId)
        )

        if not account:
            return None

        return GetAccountResponse(
            accountId=account["accountId"],
            brandId=account["brandId"],
            userId=account["userId"],
            name=account["name"],
            #
            # TODO: Passing the accessToken and accessSecret is not necessary in all cases
            #
            accessToken=account["accessToken"],
            accessTokenSecret=account["accessSecret"]
        )
