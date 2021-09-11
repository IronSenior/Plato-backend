from abc import ABC
from ...domain.account.model.account_id import AccountId


class GetTweetsService(ABC):

    def getPendingTweets(self):
        raise NotImplementedError()

    def getTweetsByAccount(self, accountId: AccountId,
                           afterDate: float, beforeDate: float):
        raise NotImplementedError()
