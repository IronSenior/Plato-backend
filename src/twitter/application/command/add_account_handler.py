from ....shared.domain.user_id import UserId
from commandbus import CommandHandler
from ...domain.repository.accounts import Accounts
from ...domain.exceptions.account_id_already_registered import AccountIdAlreadyRegistered
from ...domain.model.account import Account
from ...domain.model.account_id import AccountId
from ...domain.model.account_name import AccountName
from ....brand.domain.model.brand_id import BrandId
from ...domain.model.oauth_token import OauthToken
from ...domain.model.oauth_verifier import OauthVerifier
from .add_account_command import AddAccountCommand
from dependency_injector.wiring import inject, Provide


class AddAccountHandler(CommandHandler):

    @inject
    def __init__(self, accounts: Accounts = Provide["ACCOUNTS"]):
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
            oauthToken=OauthToken.fromString(cmd.oauthToken),
            oauthVerifier=OauthVerifier.fromString(cmd.oauthVerifier)
        )
        self.__accounts.save(account)
