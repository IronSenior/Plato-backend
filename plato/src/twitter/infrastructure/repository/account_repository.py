from ...domain.account.repository.accounts import Accounts
from ...domain.account.model.account import Account
from ...domain.account.model.account_id import AccountId
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from typing import List, Optional
from eventsourcing.application import Application


class AccountRepository(Application, Accounts):

    def __init__(self):
        self.__accounts: List[Account] = []
        return super(AccountRepository, self).__init__()

    def save(self, account: Account):
        for event in account.pending_events:
            PlatoEventBus.emit(event.bus_string, event)
        super(AccountRepository, self).save(account)

    def getById(self, accountId: AccountId) -> Optional[Account]:
        for account in self.__accounts:
            if accountId.value == account.id:
                return account
