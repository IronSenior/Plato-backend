from ...domain.account.model.account import Account
from ...application.account_dto import AccountDTO


class AccountMapper:

    @staticmethod
    def from_aggregate_to_dto(account: Account):
        return AccountDTO(
            accountId=str(account.id),
            userId=str(account.userId),
            brandId=str(account.brandId),
            name=account.name,
            oauthToken=account.accessToken,
            oauthVerifier=account.accessTokenSecret
        )
