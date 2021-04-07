from passlib.hash import sha256_crypt
import re


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
    
    def verify(self, password: str):
        return sha256_crypt.verify(password, self.__value)