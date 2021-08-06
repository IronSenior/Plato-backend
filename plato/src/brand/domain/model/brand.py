from .brand_id import BrandId
from .brand_image import BrandImageUrl
from .brand_name import BrandName
from ....shared.domain.user_id import UserId
from eventsourcing.domain import Aggregate, AggregateCreated
from typing import Optional


class Brand(Aggregate):

    def __init__(self, userId: UserId, name: BrandName,
                 image: BrandImageUrl, *args, **kwargs) -> None:
        super(Brand, self).__init__(*args, **kwargs)
        self._name: BrandName = name
        self._userId: UserId = userId
        self._image: BrandImageUrl = image

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name.value

    @property
    def userId(self):
        return self._userId.value

    @property
    def image(self):
        return self._image.value

    @classmethod
    def add(cls, id: BrandId, userId: UserId,
            name: BrandName, image: BrandImageUrl):
        return cls._create(
            cls.BrandWasCreated,
            id=id.value,
            userId=str(userId.value),
            name=name.value,
            image=image.value
        )

    class BrandWasCreated(AggregateCreated):
        bus_string = "BRAND_WAS_CREATED"
        userId: str
        name: str
        image: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            brand = super().mutate(obj)
            brand._userId = UserId.fromString(self.userId)
            brand._name = BrandName.fromString(self.name)
            brand._image = BrandImageUrl.fromString(self.image)
            return brand
