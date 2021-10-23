from plato_cqrs import QueryResponse


class GetAccountsResponse(QueryResponse):

    def __init__(self, accounts: list = []):
        self.__accounts: list = accounts

    @property
    def accounts(self):
        return self.__accounts

    def appendAccount(self, accountId: str, userId: str,
                      brandId: str, name: str):
        self.__accounts.append({
            "accountId": accountId,
            "userId": userId,
            "brandId": brandId,
            "name": name
        })
