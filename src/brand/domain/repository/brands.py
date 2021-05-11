from abc import ABC, abstractmethod
from typing import Optional, List
from ..model.brand_id import BrandId
from ..model.brand import Brand
from ....shared.domain.user_id import UserId


class Brands(ABC):

    @abstractmethod
    def save(self, brand: Brand) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getById(self, id: BrandId) -> Optional[Brand]:
        raise NotImplementedError()

    @abstractmethod
    def getByUserId(self, userId: UserId) -> Optional[List[Brand]]:
        raise NotImplementedError()
