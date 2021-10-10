import os
import pymongo


class TwitterCredentialRetriever:

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["TwitterCredentials"]

    def saveCredentials(self, token: str, secret: str):
        self.__db.insert_one({
            "token": token,
            "secret": secret
        })

    def getSecretByToken(self, token: str) -> str:
        credentials = self.__db.find_one({"token": token})
        return credentials["secret"]
