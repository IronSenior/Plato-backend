from abc import ABC, abstractmethod
from typing import Optional
from ..model.brand_id import BrandId
from ..model.brand import Brand


class Brands(ABC):

    @abstractmethod
    def save(self, brand: Brand) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getById(self, id: BrandId) -> Optional[Brand]:
        raise NotImplementedError()
