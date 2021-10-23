from abc import ABC, abstractmethod
from ...account.model.account import Account


class AccountStatusRetriever(ABC):

    @abstractmethod
    def withAccount(self, account: Account) -> dict:
        raise NotImplementedError()
