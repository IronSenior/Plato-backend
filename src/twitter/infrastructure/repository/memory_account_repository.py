from ...domain.account.repository.accounts import Accounts
from ...domain.account.model.account import Account
from ...domain.account.model.account_id import AccountId
from ....shared.domain.user_id import UserId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from typing import List, Optional
from eventsourcing.application import Application


class MemoryAccountRepository(Application, Accounts):

    def __init__(self):
        self.__accounts: List[Account] = []
        return super(MemoryAccountRepository, self).__init__()

    def save(self, account: Account):
        super(MemoryAccountRepository, self).save(account)
        self.__accounts.append(account)
        for event in account.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, accountId: AccountId) -> Optional[Account]:
        for account in self.__accounts:
            if accountId.value == account.id:
                return account

    def getByUserId(self, userId: UserId) -> Optional[List[Account]]:
        accounts = []
        for account in self.__accounts:
            if userId.value == account.userId:
                accounts.append(account)
        return accounts
