from simpleCQRS import Query


class GetUserByEmailQuery(Query):

    def __init__(self, email: str):
        self.__email: str = email

    @property
    def email(self):
        return self.__email
