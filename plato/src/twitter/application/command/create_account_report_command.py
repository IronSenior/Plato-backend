from plato_cqrs import Command


class CreateAccountReportCommand(Command):

    def __init__(self, accountId: str):
        self.__accountId: str = accountId

    @property
    def accountId(self):
        return self.__accountId
