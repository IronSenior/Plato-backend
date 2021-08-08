from ...application.query.get_account_response import GetAccountResponse
from ...application.account_dto import AccountDTO


class AccountMapper:

    @staticmethod
    def from_response_to_dto(account: GetAccountResponse) -> AccountDTO:
        return AccountDTO(
            accountId=str(account.accountId),
            userId=str(account.userId),
            brandId=str(account.brandId),
            name=account.name,
            oauthToken=account.accessToken,
            oauthVerifier=account.accessTokenSecret
        )
