from ....shared.domain.user_id import UserId
from plato_cqrs import CommandHandler
from ...domain.account.repository.accounts import Accounts
from ...domain.account.exceptions.account_id_already_registered import AccountIdAlreadyRegistered
from ...domain.account.model.account import Account
from ...domain.account.model.account_id import AccountId
from ...domain.account.model.account_name import AccountName
from ....brand.domain.model.brand_id import BrandId
from ...domain.account.model.access_token import AccessToken
from ...domain.account.model.access_token_secret import AccessTokenSecret
from .add_account_command import AddAccountCommand
from dependency_injector.wiring import inject, Provide


class AddAccountHandler(CommandHandler):

    @inject
    def __init__(self, accounts: Accounts = Provide["TWITTER_ACCOUNTS"]):
        self.__accounts: Accounts = accounts

    def handle(self, cmd: AddAccountCommand):
        accountId: AccountId = AccountId.fromString(cmd.accountId)

        if type(self.__accounts.getById(accountId)) == Account:
            raise AccountIdAlreadyRegistered("Account with ID ->", accountId.value)

        account: Account = Account.add(
            accountId=accountId,
            brandId=BrandId.fromString(cmd.brandId),
            userId=UserId.fromString(cmd.userId),
            name=AccountName.fromString(cmd.name),
            accessToken=AccessToken.fromString(cmd.accessToken),
            accessTokenSecret=AccessTokenSecret.fromString(cmd.accessTokenSecret)
        )
        self.__accounts.save(account)
