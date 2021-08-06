from passlib.hash import sha256_crypt


class UserPassword():

    def __init__(self, password: str):
        self.__value = password

    @staticmethod
    def fromString(password: str):
        return UserPassword(sha256_crypt.hash(password))

    @staticmethod
    def fromHash(password: str):
        return UserPassword(password)

    @property
    def value(self):
        return self.__value
