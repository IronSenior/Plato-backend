from ....user.domain.model.user_id import UserId
from commandbus import CommandHandler
from ...domain.repository.accounts import Accounts
from ...domain.exceptions.sn_account_id_already_registered import SocialNetworkAccountIdAlreadyRegistered
from ...domain.model.social_network_account import SocialNetworkAccount
from ...domain.model.social_network_account_id import SocialNetworkAccountId
from ...domain.model.social_network_account_name import SocialNetworkAccountName
from ....socialNetworkGroup.domain.model.social_network_group_id import SocialNetworkGroupId
from ...domain.model.social_network import SocialNetwork
from ...domain.model.user_token import UserToken
from .add_sn_account_command import AddSocialNetworkAccountCommand
from dependency_injector.wiring import inject, Provide


class AddSocialNetworkAccountHandler(CommandHandler):

    @inject
    def __init__(self, accounts: Accounts = Provide["ACCOUNTS"]):
        self.__accounts: Accounts = accounts

    def handle(self, cmd: AddSocialNetworkAccountCommand):
        accountId: SocialNetworkAccountId = SocialNetworkAccountId.fromString(cmd.accountId)

        if type(self.__accounts.getById(accountId)) == SocialNetworkAccount:
            raise SocialNetworkAccountIdAlreadyRegistered("Account with ID ->", accountId.value)

        account: SocialNetworkAccount = SocialNetworkAccount.add(
            accountId=accountId,
            snGroupId=SocialNetworkGroupId.fromString(cmd.snGroupId),
            userId=UserId.fromString(cmd.userId),
            name=SocialNetworkAccountName.fromString(cmd.name),
            userToken=UserToken.fromString(cmd.userToken),
            socialNetwork=SocialNetwork.fromString(cmd.socialNetwork)
        )
        self.__accounts.save(account)
