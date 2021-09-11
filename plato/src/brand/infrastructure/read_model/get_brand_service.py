from ...application.service.get_brand_service import GetBrandService
from ....shared.domain.user_id import UserId
from ...application.brand_dto import BrandDTO
import pymongo
from typing import List
import os


class GetBrandMongoService(GetBrandService):

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["brands"]

    def getBrandByUser(self, userId: UserId) -> List[BrandDTO]:
        brands = list(self.__db.find({"userId": str(userId.value)}))
        return brands
