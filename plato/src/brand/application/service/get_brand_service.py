from abc import ABC, abstractmethod
from ....shared.domain.user_id import UserId
from ..brand_dto import BrandDTO
from typing import List


class GetBrandService(ABC):

    @abstractmethod
    def getBrandByUser(self, userId: UserId) -> List[BrandDTO]:
        raise NotImplementedError()
