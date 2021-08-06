import re


class UserMail():

    class BadFormedEmail(Exception):
        pass

    def __init__(self, usermail: str):
        self.checkIsMail(usermail)
        self.__value = usermail

    @staticmethod
    def fromString(usermail: str):
        return UserMail(usermail)

    @property
    def value(self):
        return self.__value

    def checkIsMail(self, usermail):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", usermail):
            raise self.BadFormedEmail("Badformed Email")
