import unittest
import faker
from uuid import uuid4
from unittest.mock import Mock
from ..brand_mapper import BrandMapper
from ....domain.model.brand import Brand
from .....shared.domain.user_id import UserId
from ....domain.model.brand_id import BrandId
from ....domain.model.brand_image import BrandImageUrl
from ....domain.model.brand_name import BrandName
from ....application.brand_dto import BrandDTO

fake = faker.Faker()


class TestUserMapper(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedUserRepository = Mock()
        return super(TestUserMapper, self).setUp()

    def test_from_user_to_dto(self):
        brandid = BrandId.fromString(str(uuid4()))
        userid = UserId.fromString(str(uuid4()))
        name = BrandName.fromString(fake.company())
        image = BrandImageUrl.fromString(fake.image_url())
        brand = Brand.add(
            id=brandid,
            userId=userid,
            name=name,
            image=image
        )
        brandDto: BrandDTO = BrandMapper.from_aggregate_to_dto(brand)
        self.assertEqual(str(userid.value), brandDto["userid"])
        self.assertEqual(str(brandid.value), brandDto["id"])
        self.assertEqual(name.value, brandDto["name"])
        self.assertEqual(image.value, brandDto["image"])
